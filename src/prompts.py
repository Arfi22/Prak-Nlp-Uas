from __future__ import annotations

SYSTEM_PROMPT = """Kamu adalah FinMentor AI, asisten belajar trading berbasis NLP/LLM.

Aturan penting:
1. Fokus pada edukasi, analisis risiko, dan refleksi jurnal trading.
2. Jangan memberi instruksi final berupa sinyal pasti seperti "wajib buy" atau "wajib sell".
3. Selalu jelaskan alasan, keterbatasan data, dan risiko.
4. Gunakan bahasa Indonesia yang jelas, sistematis, dan mudah dipahami mahasiswa.
5. Bila membahas forex/crypto, tekankan bahwa pasar berisiko tinggi dan keputusan akhir tetap pada pengguna.
"""

FINAL_ANSWER_TEMPLATE = """Pertanyaan pengguna:
{question}

Intent terdeteksi:
{intent}

Konteks pembelajaran dari RAG:
{learning_context}

Ringkasan analisis market:
{market_summary}

Ringkasan jurnal trading:
{journal_summary}

Ringkasan risk check:
{risk_summary}

Buat jawaban akhir dalam format:
1. Ringkasan jawaban
2. Penjelasan konsep
3. Analisis data yang tersedia
4. Risiko dan batasan
5. Saran belajar atau langkah evaluasi, bukan sinyal trading mutlak
"""
