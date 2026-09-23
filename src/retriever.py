from src.vectorstore import create_vectorstore


def create_retriever(chunks, k=3):
    """
    Create a retriever from timestamp-aware transcript chunks.
    """

    vectorstore = create_vectorstore(chunks)

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )

    return retriever