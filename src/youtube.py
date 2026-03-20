import yt_dlp
import shutil

def find_js_runtimes():
    runtimes = {}
    for rt in ('deno', 'node', 'bun'):
        if shutil.which(rt):
            runtimes[rt] = {}
    return runtimes

url = input()

js_runtimes = find_js_runtimes()
if not js_runtimes:
    print("YouTube 다운로드에 필요한 JS 런타임이 없습니다. deno, node, bun 중 하나를 설치하세요.")
    exit(1)

ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'bestvideo*+bestaudio/best',
    'merge_output_format': 'mp4',
    'remote_components': ['ejs:github'],
    'postprocessor_args': {'merger': ['-c:a', 'aac']},
    'js_runtimes': js_runtimes,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])