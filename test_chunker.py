from src.youtube import get_transcript
from src.chunker import create_chunks


url =  "https://www.youtube.com/watch?v=8TlukLu11Yo"


print("Getting transcript...")

transcript = get_transcript(url)

print(
    f"Transcript segments: {len(transcript)}"
)


print("\nCreating chunks...")

chunks = create_chunks(
    transcript,
    max_chars=2000
)


print(
    f"Total chunks: {len(chunks)}"
)


for i, chunk in enumerate(chunks[:5]):

    print("\n" + "=" * 70)

    print(f"CHUNK {i + 1}")

    print(
        f"Start: {chunk['start']:.2f}s"
    )

    print(
        f"End: {chunk['end']:.2f}s"
    )

    print(
        f"Duration: "
        f"{chunk['end'] - chunk['start']:.2f}s"
    )
    print(f"Start Timestamp: {chunk['start_timestamp']}")
    print(f"End Timestamp: {chunk['end_timestamp']}")
    print("\nTEXT:")

    print(chunk["text"][:1000])