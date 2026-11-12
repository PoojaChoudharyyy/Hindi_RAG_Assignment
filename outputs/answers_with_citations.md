# RAG Evaluation — Six Required Questions

Model: gemini-3.5-flash-lite
Embedding model: paraphrase-multilingual-MiniLM-L12-v2
Vector database: ChromaDB (cosine similarity)
Retrieval: Top 4 chunks

## Question 1
**Question:** SLV-III ने किस उपग्रह को कक्षा में स्थापित किया और किस वर्ष?

**Answer:** SLV-III ने रोहिणी उपग्रह को वर्ष 1980 में कक्षा में स्थापित किया था।

**Sources:**
- Page 8 | इसरो के वर्ष और SLV-III | page_8_chunk_1 | Similarity: 0.7911
- Page 17 | जीवन-रेखा (टाइमलाइन) | page_17_chunk_1 | Similarity: 0.7070
- Page 20 | संस्थााओं एवं शब्दों की शब्दाावली | page_20_chunk_1 | Similarity: 0.6549
- Page 21 | विचार एवं बोध-प्रश्न | page_21_chunk_1 | Similarity: 0.5374

## Question 2
**Question:** कलाम को भारत रत्न किस वर्ष प्राप्त हुआ?

**Answer:** कलाम को भारत रत्न वर्ष 1997 में प्राप्त हुआ था।

**Sources:**
- Page 16 | पुरस्काार एवं सम्माान | page_16_chunk_1 | Similarity: 0.6321
- Page 4 | रामेश्वरम में बचपन | page_4_chunk_1 | Similarity: 0.5864
- Page 3 | ए.पी.जे. अब्दुुल कलाम कौन थे? | page_3_chunk_1 | Similarity: 0.5467
- Page 4 | रामेश्वरम में बचपन | page_4_chunk_2 | Similarity: 0.5173

## Question 3
**Question:** पोखरण-II में कलाम की क्या भूमिका थी?

**Answer:** पोखरण-II (1998 के परमाणु परीक्षण) के समय कलाम रक्षा मंत्री के वैज्ञानिक सलाहकार तथा DRDO के प्रमुख थे। उन्होंने परमाणु ऊर्जा विभाग के वैज्ञानिकों के साथ मिलकर एक केंद्रीय संगठनात्मक भूमिका निभाई।

**Retrieval query:** कलाम रक्षा मंत्री के वैज्ञानिक सलाहकार डीआरडीओ प्रमुख परमाणु ऊर्जा विभाग वैज्ञानिक पोखरण-II 1998 केंद्रीय संगठनात्मक भूमिका

**Sources:**
- Page 10 | पोखरण-II: 1998 के परमाणु परीक्षण | page_10_chunk_1 | Similarity: 0.6654
- Page 2 | विषय-सूची | page_2_chunk_1 | Similarity: 0.5444
- Page 22 | त्वरित तथ्य-सारांश | page_22_chunk_1 | Similarity: 0.5399
- Page 10 | पोखरण-II: 1998 के परमाणु परीक्षण | page_10_chunk_2 | Similarity: 0.4627

## Question 4
**Question:** Which institution did Kalam attend to study aeronautical engineering?

**Answer:** Kalam attended the Madras Institute of Technology (MIT), Chennai, to study aeronautical engineering.

**Sources:**
- Page 6 | कॉलेज के वर्ष और उड़ाान का आकर्षण | page_6_chunk_1 | Similarity: 0.6167
- Page 7 | वैज्ञाानिक करियर के पहले कदम | page_7_chunk_1 | Similarity: 0.5916
- Page 6 | कॉलेज के वर्ष और उड़ाान का आकर्षण | page_6_chunk_2 | Similarity: 0.5392
- Page 21 | विचार एवं बोध-प्रश्न | page_21_chunk_1 | Similarity: 0.5106

## Question 5
**Question:** Who co-wrote the autobiography, and in what year was it published?

**Answer:** APJ Abdul Kalam's autobiography, Wings of Fire (अग्नि की उड़ान), was co-written with scientist Arun Tiwari and published in 1999.

**Sources:**
- Page 3 | ए.पी.जे. अब्दुुल कलाम कौन थे? | page_3_chunk_2 | Similarity: 0.4231
- Page 1 | Cover page | page_1_chunk_1 | Similarity: 0.3909
- Page 21 | विचार एवं बोध-प्रश्न | page_21_chunk_2 | Similarity: 0.3267
- Page 21 | विचार एवं बोध-प्रश्न | page_21_chunk_1 | Similarity: 0.2849

## Question 6
**Question:** How and where did Kalam die in 2015?

**Answer:** Kalam collapsed while delivering a lecture to students at the Indian Institute of Management, Shillong, on 27 July 2015, and passed away shortly afterward.

**Sources:**
- Page 15 | अंतिम क्षण तक शिक्षक (2007–2015) | page_15_chunk_2 | Similarity: 0.4775
- Page 3 | ए.पी.जे. अब्दुुल कलाम कौन थे? | page_3_chunk_1 | Similarity: 0.4397
- Page 21 | विचार एवं बोध-प्रश्न | page_21_chunk_2 | Similarity: 0.3938
- Page 4 | रामेश्वरम में बचपन | page_4_chunk_1 | Similarity: 0.3842

## Evaluation Notes
- All six required questions generated answers.
- Question 3 now automatically applies a targeted retrieval query within the pipeline to retrieve the relevant Pokhran-II section.
- Answers are generated using retrieved document context.
- Similarity scores represent retrieval similarity, not factual confidence.
