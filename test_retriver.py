from src.youtube import get_transcript
from src.chunker import create_chunks
from src.retriever import create_retriever


url = "https://www.youtube.com/watch?v=ZVWg18AXXuE"

print("1. Getting transcript...")
transcript = get_transcript(url)

print("2. Creating chunks...")
chunks = create_chunks(transcript, max_chars=2000)

print("3. Creating retriever...")
retriever = create_retriever(chunks, k=3)

print("4. Testing retriever...")

query = "What is the main topic of the video?"

results = retriever.invoke(query)

print(f"\nRetrieved {len(results)} documents")

for i, document in enumerate(results):

    print("\n" + "=" * 70)
    print(f"RESULT {i + 1}")

    print("\nTEXT:")
    print(document.page_content)

    print("\nMETADATA:")
    print(document.metadata)