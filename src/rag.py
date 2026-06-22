from __future__ import annotations

from pathlib import Path
from functools import lru_cache

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_DIR = Path("data/knowledge")


def load_local_knowledge() -> list[Document]:
    docs: list[Document] = []
    for path in KNOWLEDGE_DIR.glob("*.md"):
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": str(path.name)},
            )
        )
    return docs


@lru_cache(maxsize=1)
def build_vector_store() -> InMemoryVectorStore:
    """Membangun vector store in-memory untuk RAG.

    Fungsi ini memakai:
    - LangChain Document
    - RecursiveCharacterTextSplitter
    - OpenAIEmbeddings
    - InMemoryVectorStore
    """
    docs = load_local_knowledge()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(chunks)
    return vector_store


def retrieve_context(query: str, k: int = 4) -> str:
    vector_store = build_vector_store()
    results = vector_store.similarity_search(query, k=k)
    if not results:
        return "Tidak ada konteks yang relevan dari basis pengetahuan lokal."

    formatted = []
    for i, doc in enumerate(results, start=1):
        formatted.append(
            f"[Sumber {i}: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        )
    return "\n\n".join(formatted)
