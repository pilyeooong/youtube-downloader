#!/usr/bin/env python3
"""
YouTube Downloader macOS App Builder
PyInstaller를 사용해서 macOS용 .app 번들을 생성하는 스크립트
"""

import os
import subprocess
import sys

def build_mac_app():
    """PyQt5 GUI 버전을 macOS .app 번들로 빌드"""
    
    cmd = [
        'pyinstaller',
        '--onefile',                    # 단일 실행파일
        '--windowed',                   # GUI 모드 (콘솔 숨김)
        '--name=YouTube-Downloader',    # 앱 이름
        '--icon=../assets/youtube_downloader_icon.icns',  # YouTube 스타일 아이콘
        '--osx-bundle-identifier=com.youtube.downloader',  # 번들 식별자
        '--hidden-import=PyQt5',
        '--hidden-import=yt_dlp',
        '--hidden-import=urllib3',
        '--hidden-import=certifi',
        '--hidden-import=requests',
        '../src/youtube_gui_pyqt.py'
    ]
    
    print("macOS .app 번들 빌드 시작...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("빌드 성공!")
        print(f".app 번들 위치: dist/YouTube-Downloader.app")
        print("실행 방법: open dist/YouTube-Downloader.app")
        
        # 실행 권한 확인
        app_executable = "dist/YouTube-Downloader.app/Contents/MacOS/YouTube-Downloader"
        if os.path.exists(app_executable):
            os.chmod(app_executable, 0o755)
            print("실행 권한 설정 완료")
        
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        
    except FileNotFoundError:
        print("PyInstaller가 설치되어 있지 않습니다.")
        print("pip install pyinstaller로 설치하세요.")

def build_dmg():
    """DMG 파일 생성 (선택사항)"""
    
    if not os.path.exists("dist/YouTube-Downloader.app"):
        print("먼저 .app 번들을 빌드하세요.")
        return
    
    try:
        # DMG 생성 명령
        cmd = [
            'hdiutil', 'create', '-volname', 'YouTube Downloader',
            '-srcfolder', 'dist/YouTube-Downloader.app',
            '-ov', '-format', 'UDZO',
            'dist/YouTube-Downloader.dmg'
        ]
        
        subprocess.run(cmd, check=True)
        print("DMG 파일 생성 완료: dist/YouTube-Downloader.dmg")
        
    except subprocess.CalledProcessError as e:
        print(f"DMG 생성 실패: {e}")

if __name__ == "__main__":
    print("YouTube Downloader macOS App Builder")
    print("1. .app 번들 생성")
    print("2. .app 번들 + DMG 생성")
    
    choice = input("선택하세요 (1 또는 2): ").strip()
    
    build_mac_app()
    
    if choice == "2":
        build_dmg()