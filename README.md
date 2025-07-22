# YouTube Downloader

YouTube 동영상 및 음성을 다운로드할 수 있는 Python 기반 도구입니다.

## 주요 기능

- YouTube 동영상 다운로드 (다양한 품질 지원)
- MP3 음성 추출
- GUI 인터페이스 제공 (PyQt5)
- Windows 실행 파일(.exe) 생성 지원

## 프로젝트 구조

```
youtube-download/
├── src/                      # 소스 코드
│   ├── youtube.py           # 기본 CLI 버전
│   ├── youtube_gui_pyqt.py  # GUI 버전 (PyQt5)
│   └── only_mp3.py          # MP3 전용 다운로더
├── scripts/                 # 빌드 스크립트
│   ├── build_exe.py         # EXE 파일 생성 (Python)
│   ├── build_exe.bat        # EXE 파일 생성 (Windows 배치)
│   ├── build_mac_app.py     # macOS 앱 생성
│   └── create_icon.py       # 아이콘 생성 스크립트
├── assets/                  # 리소스 파일
│   ├── youtube_downloader_icon.png  # 아이콘 (PNG)
│   ├── youtube_downloader_icon.ico  # 아이콘 (Windows)
│   └── youtube_downloader_icon.icns # 아이콘 (macOS)
└── README.md                # 프로젝트 설명
```

## 설치 및 실행

### 1. 의존성 설치

```bash
# 가상환경 생성 (권장)
pyenv virtualenv youtube-download
pyenv activate youtube-download

# 필수 패키지 설치
pip install yt-dlp PyQt5
```

### 2. 사용법

#### CLI 버전
```bash
python src/youtube.py
# URL 입력 후 다운로드
```

#### GUI 버전
```bash
python src/youtube_gui_pyqt.py
```

GUI에서 제공하는 기능:
- URL 입력
- 저장 경로 선택
- 품질 선택 (최고품질/720p/480p/MP3)
- 실시간 진행상황 표시

#### MP3 전용 버전
```bash
python src/only_mp3.py
```

### 3. Windows EXE 파일 생성

#### Python 스크립트 사용
```bash
cd scripts
python build_exe.py
```

#### Windows 배치파일 사용
Windows에서 `scripts/build_exe.bat` 파일을 더블클릭하여 실행

#### macOS 앱 번들 생성
```bash
cd scripts
python build_mac_app.py
```

## 요구사항

- Python 3.8+
- yt-dlp
- PyQt5 (GUI 버전 사용시)
- pyinstaller (EXE 파일 생성시)

## 지원 형식

### 동영상 품질
- 최고 품질 (best)
- 720p
- 480p

### 음성 형식
- MP3 (192kbps)

## 주의사항

- YouTube의 이용약관을 준수하세요
- 저작권이 있는 콘텐츠의 무단 다운로드는 금지됩니다
- 개인적인 용도로만 사용하세요

## 라이선스

이 프로젝트는 개인 사용 목적으로 만들어졌습니다.