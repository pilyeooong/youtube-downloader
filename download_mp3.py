import yt_dlp

def download_mp3(youtube_url, output_path="."):
    ydl_opts = {
        'format': 'bestaudio/best',        # 최적의 오디오 품질로 다운로드
        'extractaudio': True,             # 오디오만 추출
        'audioformat': 'mp3',             # MP3 형식으로 변환
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # 파일 저장 경로 및 이름 지정
        'postprocessors': [{              # 변환 후처리
            'key': 'FFmpegExtractAudio',  # FFmpeg을 사용하여 오디오 추출
            'preferredcodec': 'mp3',      # MP3 형식으로 저장
            'preferredquality': '192',    # 오디오 품질 (192kbps)
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])  # URL 다운로드 실행

youtube_url = input()
download_mp3(youtube_url)