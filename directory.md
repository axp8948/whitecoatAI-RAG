whitecoat-ai/
│
├── app.py                    # Streamlit entry point
│
├── db.py                     # MongoDB interactions
│
├── config/
│   ├── settings.py           # API keys, model names
│   └── constants.py          # chunk sizes, k-values, etc.
│
├── ingestion/
│   ├── extractor.py          # PDF/TXT extraction
│   ├── chunker.py            # text chunking logic
│   ├── embedder.py           # embedding generation
│   └── lab_parser.py         # structured lab value extraction
│
├── rag/
│   ├── retriever.py          # similarity search
│   ├── ranker.py             # optional reranking
│   ├── prompt_builder.py     # grounded prompt templates
│   └── generator.py          # calls Gemini to generate answer
│
├── knowledge_base/
│   ├── raw_docs/             # curated lab explanation PDFs
│   ├── processed/            # chunked + embedded KB
│   └── build_kb.py           # script to build vector index
│
├── utils/
│   ├── similarity.py         # cosine similarity
│   ├── safety.py             # medical safety filters
│   └── logger.py
│
├── tests/
│   ├── test_retrieval.py
│   ├── test_chunking.py
│   └── test_lab_parser.py
│
├── requirements.txt
└── .env



UPLOAD REPORT
     ↓
Extraction Layer (already built)
     ↓
Structured Labs
     ↓
Create Lab-Based Chunks
     ↓
Embed & Store in Vector Index

+ Curated Medical Knowledge Base
     ↓
Chunk & Embed
     ↓
Store in Same Vector Index

----------------------------------

User Question or Summary Task
     ↓
Embed Query
     ↓
Semantic Retrieval (Top-K)
     ↓
Merge Context
     ↓
Strict Grounded Prompt
     ↓
Gemini Generation