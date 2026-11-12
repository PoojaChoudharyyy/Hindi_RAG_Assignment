# Hindi Document RAG Pipeline

A Retrieval-Augmented Generation system for answering questions from a Hindi PDF about Dr. APJ Abdul Kalam.

## Features
- PDF extraction using PyMuPDF
- Hindi Unicode normalization
- Sentence-aware chunking with overlap
- Multilingual embeddings
- ChromaDB vector storage
- Semantic search and retrieval
- Gemini-powered answer generation
- Source citations with page, section, chunk ID and similarity score

## Technologies
- Python
- PyMuPDF
- Sentence Transformers
- ChromaDB
- Google Gemini API

## Models
Embedding: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

LLM: gemini-3.5-flash-lite

## Chunking Strategy
Text is divided into sentence-aware chunks of approximately 800 characters, with an overlap of approximately 120 characters.

## Vector Database
ChromaDB with cosine similarity. The top 4 relevant chunks are retrieved for each question.

## Hindi Language Handling
Text is normalized using Unicode NFC. Whitespace is cleaned, and multilingual embeddings support Hindi and English queries.

## Setup
Install dependencies:

    pip install -r requirements.txt

Place the PDF in the data folder.

Configure the Gemini API key using the GEMINI_API_KEY environment variable, or use the Google Colab secret named Gemini_API_Key.

## Run

    python src/rag_pipeline.py

Type exit to stop the interactive pipeline.

## Evaluation
Tested on six questions covering SLV-III, Bharat Ratna, Pokhran-II, aeronautical engineering, the autobiography, and Kalam's death.

All six questions generated correct answers with source citations.

## Limitations
- Answers depend on the supplied PDF.
- OCR is not implemented for scanned documents.
- Retrieval quality depends on query wording.
- The system cannot reliably answer questions outside the document.
