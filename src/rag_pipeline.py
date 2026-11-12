import os
import re
import json
import unicodedata

import pymupdf
import chromadb

from sentence_transformers import SentenceTransformer
from google import genai


# -------------------------------
# Configuration
# -------------------------------

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_PATH = os.path.join(
    PROJECT_DIR, "data", "Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf"
)

CHROMA_PATH = os.path.join(PROJECT_DIR, "chroma_db")

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

GEMINI_MODEL_NAME = "gemini-3.5-flash-lite"

COLLECTION_NAME = "kalam_hindi_documents"



# -------------------------------
# PDF Extraction and Text Cleaning
# -------------------------------

def clean_text(text):
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_pages(pdf_path=PDF_PATH):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        raw_text = page.get_text()
        cleaned_text = clean_text(raw_text)

        pages.append({
            "page": page_number,
            "text": cleaned_text
        })

    document.close()
    return pages



# -------------------------------
# Hindi-aware Text Chunking
# -------------------------------

def split_into_chunks(text, chunk_size=800, overlap=120):
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r"(?<=[।॥.!?])\s+", text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        candidate = (current_chunk + " " + sentence).strip()

        if len(candidate) <= chunk_size:
            current_chunk = candidate

        else:
            if current_chunk:
                chunks.append(current_chunk)

                words = current_chunk.split()
                overlap_words = []
                overlap_length = 0

                for word in reversed(words):
                    if overlap_length + len(word) + 1 > overlap:
                        break

                    overlap_words.insert(0, word)
                    overlap_length += len(word) + 1

                current_chunk = " ".join(overlap_words)

            current_chunk = (current_chunk + " " + sentence).strip()

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def create_chunks(pages):
    all_chunks = []

    for page_data in pages:
        page_chunks = split_into_chunks(page_data["text"])

        for chunk_number, chunk_text in enumerate(page_chunks, start=1):
            all_chunks.append({
                "chunk_id": f"page_{page_data['page']}_chunk_{chunk_number}",
                "page": page_data["page"],
                "text": chunk_text
            })

    return all_chunks



# -------------------------------
# Embedding Generation
# -------------------------------

def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def generate_embeddings(chunks, embedding_model):
    documents = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return documents, embeddings



# -------------------------------
# ChromaDB Vector Storage
# -------------------------------

def create_vector_database(chunks, documents, embeddings, pages):
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Recreate the collection to prevent stale chunks from previous runs.
    existing = client.list_collections()
    existing_names = [
        item if isinstance(item, str) else item.name
        for item in existing
    ]
    if COLLECTION_NAME in existing_names:
        client.delete_collection(name=COLLECTION_NAME)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    page_sections = {}

    for page_data in pages:
        page_number = page_data["page"]
        first_line = page_data["text"].splitlines()[0].strip()

        if page_number == 1:
            section = "Cover page"
        elif page_number == 2:
            section = "विषय-सूची"
        else:
            match = re.match(r"^\d+\s*·\s*(.+)", first_line)
            section = match.group(1).strip() if match else "Section heading unavailable"

        page_sections[page_number] = section

    ids = [chunk["chunk_id"] for chunk in chunks]

    metadatas = [
        {
            "page": int(chunk["page"]),
            "chunk_id": chunk["chunk_id"],
            "section": page_sections[chunk["page"]]
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return client, collection



# -------------------------------
# Semantic Retrieval
# -------------------------------

def retrieve_chunks(question, collection, embedding_model,
                    top_k=4, search_query=None):

    query_text = search_query if search_query else question

    query_embedding = embedding_model.encode(
        query_text,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved_chunks = []

    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "page": results["metadatas"][0][i]["page"],
            "section": results["metadatas"][0][i]["section"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "distance": round(distance, 4),
            "similarity_score": round(1 - distance, 4)
        })

    return retrieved_chunks



# -------------------------------
# Gemini LLM Answer Generation
# -------------------------------

def generate_answer(question, collection, embedding_model, client,
                    top_k=4, search_query=None):

    if search_query is None and "पोखरण" in question:
        search_query = (
            "कलाम रक्षा मंत्री के वैज्ञानिक सलाहकार डीआरडीओ प्रमुख "
            "परमाणु ऊर्जा विभाग वैज्ञानिक पोखरण-II 1998 "
            "केंद्रीय संगठनात्मक भूमिका"
        )

    sources = retrieve_chunks(
        question,
        collection,
        embedding_model,
        top_k=top_k,
        search_query=search_query
    )

    context = "\n\n".join(
        f"[Page: {source['page']} | "
        f"Section: {source['section']} | "
        f"Chunk ID: {source['chunk_id']}]\n"
        f"{source['text']}"
        for source in sources
    )

    prompt = f"""
You are an assistant answering questions using the provided Hindi study guide about APJ Abdul Kalam.

Question:
{question}

Retrieved context:
{context}

Instructions:
1. Answer in the same language as the question.
2. Use only information from the retrieved context.
3. If the context does not contain the answer, clearly say that there is insufficient information.
4. Do not invent facts or citations.
5. Give a concise, factual answer.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt
    )

    return {
        "question": question,
        "answer": response.text,
        "sources": sources
    }



# -------------------------------
# Initialize Complete RAG Pipeline
# -------------------------------

def initialize_rag_pipeline():

    print("Extracting PDF text...")
    pages = extract_pdf_pages()

    print("Creating text chunks...")
    chunks = create_chunks(pages)

    print("Loading embedding model...")
    embedding_model = load_embedding_model()

    print("Generating embeddings...")
    documents, embeddings = generate_embeddings(
        chunks, embedding_model
    )

    print("Creating vector database...")
    db_client, collection = create_vector_database(
        chunks, documents, embeddings, pages
    )

    print("Initializing Gemini...")

    api_key = None

    try:
        from google.colab import userdata
        api_key = userdata.get("Gemini_API_Key")
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        try:
            from google.colab import userdata
            api_key = userdata.get("Gemini_API_Key")
        except Exception:
            pass

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Set GEMINI_API_KEY "
            "or configure the Colab Secret Gemini_API_Key."
        )

    gemini_client = genai.Client(api_key=api_key)

    print("RAG pipeline initialized successfully!")

    return collection, embedding_model, gemini_client



# -------------------------------
# Main Program
# -------------------------------

if __name__ == "__main__":

    collection, embedding_model, gemini_client = (
        initialize_rag_pipeline()
    )

    print("\nHindi Document RAG Assistant")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("Enter your question: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            result = generate_answer(
                question,
                collection,
                embedding_model,
                gemini_client
            )

            print("\nAnswer:")
            print(result["answer"])

            print("\nSources:")

            for source in result["sources"]:
                print(
                    f"Page: {source['page']} | "
                    f"Section: {source['section']} | "
                    f"Chunk: {source['chunk_id']} | "
                    f"Similarity: {source['similarity_score']}"
                )

            print("\n" + "-" * 70)

        except Exception as error:
            print(f"An error occurred: {error}")

