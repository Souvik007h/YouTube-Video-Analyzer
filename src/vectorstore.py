from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.embeddings import get_embedding_model


def create_vectorstore(chunks):
    """
    Convert timestamp-aware chunks into LangChain Documents
    and store them in ChromaDB.
    """

    documents = []

    for chunk in chunks:

        document = Document(
            page_content=chunk["text"],

            metadata={
                "start": chunk["start"],
                "end": chunk["end"],
                "start_timestamp": chunk["start_timestamp"],
                "end_timestamp": chunk["end_timestamp"],
                "video_id": chunk["video_id"]
            }
        )

        documents.append(document)

    print(f"Creating vector store for {len(documents)} chunks...")

    embeddings = get_embedding_model()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="data/chroma"
    )

    print("Vector store created successfully!")

    return vectorstore