#!/usr/bin/env python3
"""
YouTube Downloader EXE Builder
PyInstaller를 사용해서 Windows용 exe 파일을 생성하는 스크립트
"""

import os
import subprocess
import sys
import shutil

def build_exe():
    """PyQt5 GUI 버전을 exe로 빌드"""

    # PyInstaller 명령어 구성
    cmd = [
        'pyinstaller',
        '--onefile',                    # 단일 exe 파일로 생성
        '--windowed',                   # 콘솔 창 숨김
        '--noconfirm',
        '--name=YouTube-Downloader',    # exe 파일명
        '--icon=../assets/youtube_downloader_icon.ico',  # YouTube 스타일 아이콘
        '--hidden-import=PyQt5',
        '--hidden-import=yt_dlp',
        '--hidden-import=urllib3',
        '--hidden-import=certifi',
        '--hidden-import=requests',
    ]

    # ffmpeg/ffprobe 없으면 병합·MP3 변환이, deno 없으면 YouTube JS 챌린지가 실패한다.
    # 셋 다 필수이므로 하나라도 없으면 빌드하지 않는다 (빌드된 뒤 런타임에 터지는 편이 더 나쁘다).
    missing = []
    for name in ('ffmpeg', 'ffprobe', 'deno'):
        path = shutil.which(name)
        if path:
            cmd.append(f'--add-binary={path};.')
            print(f"{name} 포함: {path}")
        else:
            missing.append(name)

    if missing:
        print(f"오류: {', '.join(missing)} 를 PATH에서 찾을 수 없습니다.")
        print("  ffmpeg/ffprobe: https://www.gyan.dev/ffmpeg/builds/")
        print("  deno:           https://deno.com")
        return

    cmd.append('../src/youtube_gui_pyqt.py')

    print("EXE 파일 빌드 시작...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("빌드 성공!")
        print(f"EXE 파일 위치: dist/YouTube-Downloader.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        
    except FileNotFoundError:
        print("PyInstaller가 설치되어 있지 않습니다.")
        print("pip install pyinstaller 로 설치하세요.")

def build_simple_exe():
    """간단한 버전 (아이콘, ffmpeg 없이)"""
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=YouTube-Downloader',
        '--hidden-import=PyQt5',
        '--hidden-import=yt_dlp',
        '../src/youtube_gui_pyqt.py'
    ]
    
    print("간단한 EXE 파일 빌드 시작...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("빌드 성공!")
        print(f"EXE 파일 위치: dist/YouTube-Downloader.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")

if __name__ == "__main__":
    print("YouTube Downloader EXE Builder")
    print("1. 완전한 버전 (아이콘, ffmpeg 포함)")
    print("2. 간단한 버전 (기본)")
    
    choice = input("선택하세요 (1 또는 2): ").strip()
    
    if choice == "1":
        build_exe()
    else:
        build_simple_exe()