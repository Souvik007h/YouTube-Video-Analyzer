from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.embeddings import get_embedding_model


CHROMA_DIRECTORY = "data/chroma"


def create_vectorstore(chunks):
    """
    Create or reuse a Chroma collection for one YouTube video.

    Each video gets its own collection based on video_id.
    """

    if not chunks:
        raise ValueError("No chunks provided.")

    video_id = chunks[0]["video_id"]

    collection_name = f"youtube_{video_id}"

    print(
        f"Using Chroma collection: {collection_name}"
    )

    embeddings = get_embedding_model()

    # Check whether this collection already exists
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIRECTORY
    )

    # Check if collection already contains documents
    existing_count = vectorstore._collection.count()

    if existing_count > 0:

        print(
            f"Existing collection found "
            f"({existing_count} documents)."
        )

        print("Reusing existing vector store.")

        return vectorstore

    # ------------------------------------------------
    # Create documents
    # ------------------------------------------------

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

    print(
        f"Creating vector store for "
        f"{len(documents)} chunks..."
    )

    # ------------------------------------------------
    # Add documents
    # ------------------------------------------------

    vectorstore.add_documents(documents)

    print("Vector store created successfully!")

    return vectorstore