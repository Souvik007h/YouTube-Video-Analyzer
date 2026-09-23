from src.youtube import create_timestamp_url


video_id = "8TlukLu11Yo"
seconds = 279

url = create_timestamp_url(video_id, seconds)

print("Generated YouTube URL:")
print(url)