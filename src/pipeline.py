from src.youtube import get_transcript
from src.youtube_metadata import get_video_metadata
from src.chunker import create_chunks
from src.retriever import create_retriever
from src.qa_chain import create_qa_chain


def prepare_video( url: str, provider: str, model: str, api_key: str, k: int = 3):
    # ---------------------------------------------
    # 1. Get video metadata
    # ---------------------------------------------

    metadata = get_video_metadata(url)

    # ---------------------------------------------
    # 2. Get English transcript
    # ---------------------------------------------

    transcript = get_transcript(url)

    if not transcript:
        raise ValueError(
            "No English transcript was found for this video."
        )

    # ---------------------------------------------
    # 3. Create timestamp-aware chunks
    # ---------------------------------------------

    chunks = create_chunks(
        transcript,
        max_chars=2000
    )

    if not chunks:
        raise ValueError(
            "Could not create transcript chunks."
        )

    # ---------------------------------------------
    # 4. Create retriever
    # ---------------------------------------------

    retriever = create_retriever(
        chunks,
        k=k
    )

    # ---------------------------------------------
    # 5. Create QA chain
    # ---------------------------------------------

    answer_question = create_qa_chain(
        retriever=retriever,
        provider=provider,
        model=model,
        api_key=api_key
    )

    return {
        "metadata": metadata,
        "retriever": retriever,
        "answer_question": answer_question
    }