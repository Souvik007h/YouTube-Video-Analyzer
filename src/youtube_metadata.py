import os
import isodate
from datetime import datetime

from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.youtube import extract_video_id

load_dotenv()


def get_video_metadata(url: str):
    """
    Get YouTube video title, channel name, duration,
    and basic video information.
    """

    video_id = extract_video_id(url)

    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise ValueError(
            "YOUTUBE_API_KEY is missing from .env"
        )

    youtube = build(
        "youtube",
        "v3",
        developerKey=api_key
    )

    response = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    ).execute()

    if not response.get("items"):
        raise ValueError(
            "YouTube video not found or unavailable."
        )

    video = response["items"][0]

    snippet = video["snippet"]
    content_details = video["contentDetails"]

    duration_seconds = int(
        isodate.parse_duration(
            content_details["duration"]
        ).total_seconds()
    )

    return {
            "video_id": video_id,
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": format_published_date(snippet["publishedAt"]),
            "duration_seconds": duration_seconds,
            "duration": format_duration(duration_seconds),
        }

def format_duration(seconds: int) -> str:
    """
    Convert seconds into HH:MM:SS or MM:SS.
    """

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    return f"{minutes}:{seconds:02d}"


def format_published_date(date_string: str) -> str:
    """
    Convert YouTube ISO 8601 date to a readable date.
    """

    date = datetime.fromisoformat(
        date_string.replace("Z", "+00:00")
    )

    return date.strftime("%B %d, %Y")