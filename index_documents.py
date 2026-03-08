from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store

documents = load_documents("data/documents")

chunks = split_documents(documents)

embeddings = get_embeddings()

create_vector_store(
    chunks,
    embeddings,
    "data/vector_db"
)

print("Indexing complete")