from pytubefix import YouTube


def download_video(yt):
  highresvid = yt.streams.get_highest_resolution()
  # highresvid = yt.streams.filter(only_audio=True).first()
  
  # finally download the YouTube Video...
  highresvid.download()
  print("Video is Downloading as",yt.title+".mp4")
  
link = input()
# Create YouTube Object.
yt = YouTube(link, use_oauth=True, allow_oauth_cache=True) 

# call The function..
download_video(yt)
