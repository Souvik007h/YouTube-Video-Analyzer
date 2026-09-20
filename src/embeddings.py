from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_embedding_model():
    """
    Create and return the Gemini embedding model.
    """

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2"
    )

    return embeddings