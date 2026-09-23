from src.youtube import get_transcript
from src.chunker import create_chunks
from src.vectorstore import create_vectorstore


url = "https://www.youtube.com/watch?v=coQ5dg8wM2o"


print("1. Getting transcript...")

transcript = get_transcript(url)

print(
    f"Transcript segments: {len(transcript)}"
)


print("\n2. Creating chunks...")

chunks = create_chunks(
    transcript,
    max_chars=2000
)

print(
    f"Total chunks: {len(chunks)}"
)


print("\n3. Creating vector database...")

vectorstore = create_vectorstore(chunks)


print("\n4. Testing vector database...")

results = vectorstore.similarity_search_with_score(
    "What is the main topic of the video?",
    k=3
)

print(f"\nRetrieved {len(results)} documents")

for i, (result, score) in enumerate(results):

    print("\n" + "=" * 70)
    print(f"RESULT {i + 1}")

    print(f"\nDistance Score: {score:.4f}")

    print("\nTEXT:")
    print(result.page_content)

    print("\nMETADATA:")
    print(result.metadata)