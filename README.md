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

## 최종 사용자용 (개발환경 없는 PC)

파이썬·deno·ffmpeg 설치가 필요 없다. [Releases](../../releases)에서 받아 바로 실행한다.

- Windows: `YouTube-Downloader.exe`
- macOS: `YouTube-Downloader.dmg`

Python 인터프리터, ffmpeg, ffprobe, deno가 모두 실행 파일 안에 들어 있다.

> **yt-dlp는 실행 파일 안에 고정된다.** YouTube가 사양을 바꾸면 예전에 받은 exe는
> "Signature extraction failed" / "Requested format is not available" 같은 오류를 내기 시작한다.
> 이때는 코드 수정 없이 **새 태그를 밀어 exe를 다시 빌드**하면 최신 yt-dlp가 포함된다.

> Windows SmartScreen이 서명되지 않은 exe를 막으면 `추가 정보 → 실행`으로 통과시킨다.

## 개발자용 설치 및 실행

### 1. 의존성 설치

```bash
# 가상환경 생성 (권장)
pyenv virtualenv youtube-download
pyenv activate youtube-download

# 필수 패키지 설치
pip install -U -r requirements.txt
```

### 1-1. 외부 바이너리 (소스로 실행할 때 필수)

| 바이너리 | 용도 | 없으면 |
|---|---|---|
| `deno` (v2.3.0+) | YouTube JS 챌린지 해결 | 다운로드 자체가 실패 |
| `ffmpeg`, `ffprobe` | 영상+음성 병합, MP3 변환 | 병합·변환 실패 |

```bash
# macOS
brew install deno ffmpeg

# Windows (winget)
winget install DenoLand.Deno
winget install Gyan.FFmpeg
```

yt-dlp 2025.11부터 YouTube 다운로드에 외부 JS 런타임이 **필수**다. `node` v22+도 쓸 수 있다.

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

- Python 3.11+ (yt-dlp 권장 최소 버전)
- yt-dlp (최신 유지 필수 — `pip install -U yt-dlp`)
- deno v2.3.0+ 또는 node v22+ (YouTube JS 챌린지)
- ffmpeg / ffprobe (병합·MP3 변환)
- PyQt5 (GUI 버전 사용시)
- pyinstaller (EXE 파일 생성시)

## 문제 해결

| 증상 | 원인 | 조치 |
|---|---|---|
| 특정 영상만 `HTTP Error 403` | 영상별 PO Token 요구 / IP 변경 / URL 만료 | **앱이 다른 player_client로 자동 재시도한다.** 그래도 실패하면 VPN을 끄고 잠시 후 재시도 |
| `Signature extraction failed`, 화질이 낮은 것만 잡힘 | yt-dlp가 오래됨 | `pip install -U yt-dlp` / exe는 재빌드 |
| `JS 런타임을 찾을 수 없습니다` | deno·node 없음 | deno 설치 후 재시도 |
| 병합 실패, MP3 변환 실패 | ffmpeg/ffprobe 없음 | ffmpeg 설치 후 재시도 |
| exe가 실행되자마자 종료 | 백신이 임시 폴더 추출 차단 | 예외 등록 후 재실행 |

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