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
            You are an expert YouTube video analysis assistant.

            Your job is to answer the user's question using ONLY the
            provided transcript context.

            The user wants a useful, explanatory answer rather than
            a one-sentence summary.

            Follow these rules carefully:

            1. GROUNDING
            - Use ONLY information contained in the transcript context.
            - Do not use outside knowledge.
            - Do not invent facts, examples, definitions, or explanations.
            - If the retrieved context does not contain enough information,
                clearly say so.

            2. ANSWER DEPTH
            - Give a detailed but focused explanation.
            - For simple questions, give a concise explanation.
            - For conceptual or technical questions, explain the concept,
                how it works, and how it is used in the video when the
                transcript provides that information.
            - Prefer approximately 2–5 paragraphs or useful bullet points,
                depending on the question.
            - Do not unnecessarily repeat the same information.

            3. STRUCTURE
            When appropriate, organize the answer using:
            - A direct definition or answer first.
            - Key points or components.
            - How the concept is used in the video.
            - A short example only if the transcript provides one.

            4. TECHNICAL QUESTIONS
            For technical questions:
            - Explain terminology mentioned in the transcript.
            - Explain relationships between components when the transcript
                describes them.
            - Preserve technical names exactly when possible.
            - Do not add technical details that are not present in the
                transcript.

            5. TIMESTAMPS
            - Include relevant timestamps naturally in the answer.
            - Only use timestamps provided in the transcript context.
            - Do not invent timestamps.
            - Do not cite a timestamp merely because it was retrieved;
                use it when it supports the statement.

            6. MISSING INFORMATION
            If the context does not contain enough information to answer
            the question, say:

            "I could not find enough information about this in the
            retrieved video content."

            Do not fill the missing information using your own knowledge.

            7. SOURCE FOCUS
            - Prefer the most relevant retrieved sections.
            - Do not mention irrelevant retrieved sections.
            - Multiple retrieved sections may be combined when they explain
                different parts of the same answer.

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