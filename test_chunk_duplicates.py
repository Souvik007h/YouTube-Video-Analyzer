from src.youtube import get_transcript
from src.chunker import create_chunks

url = "https://www.youtube.com/watch?v=8TlukLu11Yo"

print("Getting transcript...")
transcript = get_transcript(url)

print("Creating chunks...")
chunks = create_chunks(transcript, max_chars=2000)

print(f"\nTotal chunks: {len(chunks)}")

# Check duplicate chunk texts
chunk_texts = [chunk["text"] for chunk in chunks]

unique_texts = set(chunk_texts)

print(f"Unique chunks: {len(unique_texts)}")
print(f"Duplicate count: {len(chunk_texts) - len(unique_texts)}")

# Display every chunk's timestamp
print("\nChunk timestamps:")

for i, chunk in enumerate(chunks):
    print(
        f"Chunk {i + 1}: "
        f"{chunk['start_timestamp']} - "
        f"{chunk['end_timestamp']}"
    )