from src.youtube import get_transcript, format_timestamp, create_timestamp_url, extract_video_id


url = "https://www.youtube.com/watch?v=8TlukLu11Yo"

transcript = get_transcript(url)

for item in transcript[:10]:
    print(item)
    


# print(format_timestamp(763))
# print(format_timestamp(3725))

# video_id = extract_video_id(url)
# url = create_timestamp_url(
#     video_id,
#     763
# )

# print(url)