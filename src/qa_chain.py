from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.youtube import create_timestamp_url

def create_qa_chain(retriever):
    """
    Create a RAG question-answering chain
    using Google Gemini and the video transcript retriever.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
        """
            You are a helpful YouTube video analysis assistant.

            Answer the user's question using ONLY the provided transcript context.

            Instructions:
            1. Do not invent information.
            2. If the answer is not present in the context, say:
            "I could not find the answer in the retrieved video content."
            3. Give a clear and concise answer.
            4. Include relevant timestamps when available.
            5. Use the timestamp metadata provided in the context.

            Transcript Context:
            {context}

            User Question:
            {question}

            Answer:
        """
    )

    def answer_question(question):
        documents = retriever.invoke(question)

        context_parts = []

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

            context_parts.append(
                f"""
                    Timestamp: {start_timestamp} - {end_timestamp}
                    Transcript:
                    {document.page_content}
                """
            )

        context = "\n".join(context_parts)

        formatted_prompt = prompt.format(
            context=context,
            question=question
        )

        response = llm.invoke(formatted_prompt)

        return {
            "answer": response.content[0]["text"],
            "documents": documents
        }

    return answer_question