from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

response = llm.invoke(
    "Explain RAG in one sentence."
)

print(response.content[0]["text"])