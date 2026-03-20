import yt_dlp
import shutil

def find_js_runtimes():
    runtimes = {}
    for rt in ('deno', 'node', 'bun'):
        if shutil.which(rt):
            runtimes[rt] = {}
    return runtimes

url = input("Enter YouTube URL: ")

js_runtimes = find_js_runtimes()
if not js_runtimes:
    print("YouTube 다운로드에 필요한 JS 런타임이 없습니다. deno, node, bun 중 하나를 설치하세요.")
    exit(1)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'remote_components': ['ejs:github'],
    'js_runtimes': js_runtimes,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
