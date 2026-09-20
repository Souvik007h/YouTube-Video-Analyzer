from src.youtube import format_timestamp


def create_chunks(transcript, max_chars=2000, overlap_segments=2):
    """
    Create timestamp-aware chunks from YouTube transcript.

    Each chunk contains:
        - text
        - start
        - end
        - start_timestamp
        - end_timestamp
        - video_id
    """

    chunks = []

    current_segments = []
    current_chars = 0

    for item in transcript:

        text = item["text"].strip()

        if not text:
            continue

        current_segments.append(item)
        current_chars += len(text)

        # Create chunk once it reaches max_chars
        if current_chars >= max_chars:

            chunk_text = " ".join(
                segment["text"]
                for segment in current_segments
            )

            start = current_segments[0]["start"]
            end = current_segments[-1]["end"]

            chunk = {
                "text": chunk_text,

                "start": start,
                "end": end,

                "start_timestamp": format_timestamp(start),
                "end_timestamp": format_timestamp(end),

                "video_id": current_segments[0]["video_id"]
            }

            chunks.append(chunk)

            # Keep overlap
            if overlap_segments > 0:

                current_segments = current_segments[
                    -overlap_segments:
                ]

            else:

                current_segments = []

            # Recalculate character count
            current_chars = sum(
                len(segment["text"])
                for segment in current_segments
            )

    # Add remaining segments
    if current_segments:

        chunk_text = " ".join(
            segment["text"]
            for segment in current_segments
        )

        start = current_segments[0]["start"]
        end = current_segments[-1]["end"]

        chunk = {
            "text": chunk_text,

            "start": start,
            "end": end,

            "start_timestamp": format_timestamp(start),
            "end_timestamp": format_timestamp(end),

            "video_id": current_segments[0]["video_id"]
        }

        chunks.append(chunk)

    return chunks