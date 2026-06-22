# FinMentor AI

FinMentor AI adalah aplikasi berbasis **NLP (Natural Language Processing)** dan **LLM (Large Language Model)** yang berfungsi sebagai asisten analisis keuangan.

Project ini menggunakan konsep **RAG (Retrieval Augmented Generation)** agar sistem dapat memberikan jawaban berdasarkan informasi yang tersedia.

Project ini dibuat menggunakan tiga library utama:

- LangChain
- LangGraph
- LangSmith

## Deskripsi Project

FinMentor AI merupakan sistem chatbot berbasis LLM yang dapat membantu pengguna mendapatkan informasi dan analisis terkait keuangan.

Sistem ini menggabungkan beberapa teknologi:

- Large Language Model untuk menghasilkan jawaban
- Retrieval Augmented Generation untuk mencari informasi yang relevan
- LangGraph untuk mengatur alur kerja aplikasi
- LangSmith untuk melakukan monitoring dan evaluasi

## Teknologi yang Digunakan

## 1. LangChain

LangChain digunakan untuk membangun aplikasi berbasis LLM.

Pada project ini LangChain digunakan untuk:

- Menghubungkan aplikasi dengan model LLM
- Membuat dan mengatur prompt
- Mengelola dokumen
- Membuat proses Retrieval Augmented Generation (RAG)

## 2. LangGraph

LangGraph digunakan untuk membuat workflow atau alur kerja aplikasi.

Pada project ini LangGraph digunakan untuk:

- Membuat graph proses AI
- Mengatur alur input dan output
- Menghubungkan beberapa proses menjadi satu workflow

## 3. LangSmith

LangSmith digunakan untuk melakukan monitoring dan evaluasi aplikasi LLM.

Pada project ini LangSmith digunakan untuk:

- Melakukan tracing proses LLM
- Melihat proses input sampai output
- Mengevaluasi hasil jawaban model

## Fitur Aplikasi

Fitur utama FinMentor AI:

- Chatbot berbasis Artificial Intelligence
- Pemrosesan pertanyaan menggunakan NLP
- Sistem RAG untuk pencarian informasi
- Integrasi Large Language Model
- Workflow AI menggunakan LangGraph
- Monitoring menggunakan LangSmith
- Tampilan aplikasi menggunakan Streamlit

## Struktur Project

```
Uas2/
|
├── app.py
├── requirements.txt
├── README.md
├── style.css
|
├── src/
|   ├── graph.py
|   ├── llm.py
|   ├── rag.py
|   ├── prompts.py
|   └── market_indicators.py
|
├── data/
|   ├── knowledge/
|   └── sample/
|
└── tests/
    └── evaluate_langsmith.py
```

## Cara Menjalankan Project

### 1. Clone Repository

```
git clone https://github.com/username/FinMentor-AI.git
```

Masuk ke folder project:

```
cd FinMentor-AI
```

### 2. Install Library

Install semua kebutuhan:

```
pip install -r requirements.txt
```

### 3. Membuat File Environment

Buat file baru bernama:

```
.env
```

Isi dengan API Key:

```
GROQ_API_KEY=your_api_key
LANGSMITH_API_KEY=your_api_key
LANGSMITH_TRACING=true
```

### 4. Menjalankan Aplikasi

Jalankan aplikasi menggunakan Streamlit:

```
streamlit run app.py
```

## Alur Sistem

```
User Input
      |
      v
LangGraph Workflow
      |
      v
Pemrosesan Pertanyaan
      |
      v
RAG Retrieval
      |
      v
LLM Processing
      |
      v
Jawaban User
```

## Evaluasi

LangSmith digunakan untuk melihat:

- Input pengguna
- Proses pemanggilan model
- Waktu proses
- Hasil output

## Kesimpulan

FinMentor AI berhasil mengimplementasikan sistem NLP berbasis LLM dengan menggunakan tiga library utama yaitu LangChain, LangGraph, dan LangSmith.

LangChain digunakan untuk membangun komponen LLM dan RAG.

LangGraph digunakan untuk membuat workflow sistem.

LangSmith digunakan untuk melakukan monitoring serta evaluasi.

## Author

Nama:
ARFI AKSA RIFANDY

Project:
FinMentor AI

Mata Kuliah:
NLP / LLM
