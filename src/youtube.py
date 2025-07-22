import yt_dlp

# Replace 'your_video_url' with the YouTube video URL you want to download
url = input()
# Configure options if necessary
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',  # Set filename format
    'format': 'best',  # Choose the best available quality
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])