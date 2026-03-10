from langchain_chroma import Chroma
from rag.embeddings import get_embeddings

def retrieve_context(query):
    try:
        _embeddings = get_embeddings()
        _db = Chroma(
            persist_directory="data/vector_db",
            embedding_function=_embeddings
        )
        results = _db.similarity_search_with_score(query, k=6)
    except Exception:
        return ""

    if not results:
        return ""

    filtered = [doc for doc, score in results if score < 1.3]

    if not filtered:
        return ""

    return "\n\n".join(doc.page_content for doc in filtered).strip()