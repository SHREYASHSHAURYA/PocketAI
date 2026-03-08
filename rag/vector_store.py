from langchain_community.vectorstores import Chroma

def create_vector_store(chunks, embeddings, persist_directory):

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=persist_directory
    )

    return db