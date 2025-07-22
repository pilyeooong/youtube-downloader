@echo off
echo YouTube Downloader EXE Builder for Windows
echo ==========================================

REM 가상환경 활성화 (필요한 경우)
REM call venv\Scripts\activate

echo Installing required packages...
pip install pyinstaller PyQt5 yt-dlp

echo Building EXE file...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name=YouTube-Downloader ^
  --icon=../assets/youtube_downloader_icon.ico ^
  --hidden-import=PyQt5 ^
  --hidden-import=yt_dlp ^
  --hidden-import=urllib3 ^
  --hidden-import=certifi ^
  --hidden-import=requests ^
  ../src/youtube_gui_pyqt.py

echo.
echo Build complete!
echo EXE file location: dist\YouTube-Downloader.exe
echo.
pause