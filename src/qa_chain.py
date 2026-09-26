from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.youtube import create_timestamp_url


def create_qa_chain(
    retriever,
    provider,
    model,
    api_key
):
    """
    Create a RAG question-answering chain
    using the selected LLM provider.
    """

    # --------------------------------------------------
    # Create selected LLM
    # --------------------------------------------------

    if provider == "Google Gemini":

        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0,
            max_retries=3
        )

    elif provider == "OpenAI":

        llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0,
            max_retries=3
        )

    else:

        raise ValueError(
            f"Unsupported AI provider: {provider}"
        )

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = ChatPromptTemplate.from_template(
        """
            You are a helpful YouTube video analysis assistant.

            Answer the user's question using ONLY the provided
            transcript context.

            Instructions:

            1. Do not invent information.
            2. If the answer is not present in the context, say:
            "I could not find the answer in the retrieved video content."
            3. Give a clear and concise answer.
            4. Include relevant timestamps when available.
            5. Use the timestamp metadata provided in the context.
            6. Do not use outside knowledge to answer the question.

            Transcript Context:
            {context}

            User Question:
            {question}

            Answer:
        """
    )

    # --------------------------------------------------
    # Question answering function
    # --------------------------------------------------

    def answer_question(question):

        # Retrieve relevant chunks
        documents = retriever.invoke(question)

        context_parts = []
        sources = []

        # --------------------------------------------------
        # Build context + source links
        # --------------------------------------------------

        for document in documents:

            metadata = document.metadata

            start_timestamp = metadata.get(
                "start_timestamp",
                "Unknown"
            )

            end_timestamp = metadata.get(
                "end_timestamp",
                "Unknown"
            )

            video_id = metadata.get("video_id")

            start_seconds = metadata.get(
                "start",
                0
            )

            timestamp_url = create_timestamp_url(
                video_id,
                start_seconds
            )

            context_parts.append(
                f"""
                    Timestamp: {start_timestamp} - {end_timestamp}

                    Transcript:
                    {document.page_content}
                """
            )

            sources.append({
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "url": timestamp_url
            })

        # --------------------------------------------------
        # Combine retrieved context
        # --------------------------------------------------

        context = "\n".join(context_parts)

        # --------------------------------------------------
        # Create prompt
        # --------------------------------------------------

        formatted_prompt = prompt.format(
            context=context,
            question=question
        )

        # --------------------------------------------------
        # Generate answer
        # --------------------------------------------------

        response = llm.invoke(
            formatted_prompt
        )

        # --------------------------------------------------
        # Normalize response content
        # --------------------------------------------------

        if isinstance(response.content, str):

            answer = response.content

        elif isinstance(response.content, list):

            answer_parts = []

            for block in response.content:

                if isinstance(block, dict):

                    text = block.get("text")

                    if text:
                        answer_parts.append(text)

                else:

                    answer_parts.append(str(block))

            answer = "\n".join(answer_parts)

        else:

            answer = str(response.content)

        return {
            "answer": answer,
            "documents": documents,
            "sources": sources
        }

    return answer_question