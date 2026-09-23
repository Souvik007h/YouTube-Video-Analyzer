from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    if "youtube.com/watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    if "youtube.com/shorts/" in url:
        return url.split("shorts/")[1].split("?")[0]

    raise ValueError("Invalid YouTube URL")


def get_transcript(url: str):

    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    results = []

    for item in transcript:

        results.append({
            "text": item.text,
            "start": round(item.start, 3),
            "duration": round(item.duration, 3),
            "end": round(item.start + item.duration, 3),
            "video_id": video_id
        })

    return results

def format_timestamp(seconds: float) -> str:

    seconds = int(seconds)

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    return f"{minutes}:{seconds:02d}"

def create_timestamp_url(video_id: str, seconds: float) -> str:
    """
    Create a YouTube URL that starts at a specific timestamp.
    """

    seconds = int(seconds)

    return (
        f"https://www.youtube.com/watch?v={video_id}"
        f"&t={seconds}s"
    )