@echo off
setlocal enabledelayedexpansion
echo YouTube Downloader EXE Builder for Windows
echo ==========================================

REM 가상환경 활성화 (필요한 경우)
REM call venv\Scripts\activate

echo Installing required packages...
pip install -U -r ..\requirements.txt
if errorlevel 1 goto :fail

REM ffmpeg / ffprobe / deno 를 반드시 번들해야 한다.
REM   - ffmpeg, ffprobe 없음 -> 영상+음성 병합(merge)과 MP3 변환이 실패
REM   - deno 없음            -> YouTube JS 챌린지를 못 풀어 다운로드 자체가 실패
for %%B in (ffmpeg.exe ffprobe.exe deno.exe) do (
  set "PATH_%%~nB="
  for /f "delims=" %%P in ('where %%B 2^>nul') do (
    if not defined PATH_%%~nB set "PATH_%%~nB=%%P"
  )
  if not defined PATH_%%~nB (
    echo [ERROR] %%B not found in PATH.
    echo         ffmpeg/ffprobe: https://www.gyan.dev/ffmpeg/builds/
    echo         deno:           https://deno.com
    goto :fail
  )
  echo Bundling %%B: !PATH_%%~nB!
)

echo Building EXE file...
pyinstaller ^
  --onefile ^
  --windowed ^
  --noconfirm ^
  --name=YouTube-Downloader ^
  --icon=..\assets\youtube_downloader_icon.ico ^
  --hidden-import=PyQt5 ^
  --hidden-import=yt_dlp ^
  --hidden-import=urllib3 ^
  --hidden-import=certifi ^
  --hidden-import=requests ^
  --add-binary="!PATH_ffmpeg!;." ^
  --add-binary="!PATH_ffprobe!;." ^
  --add-binary="!PATH_deno!;." ^
  ..\src\youtube_gui_pyqt.py
if errorlevel 1 goto :fail

echo.
echo Build complete!
echo EXE file location: dist\YouTube-Downloader.exe
echo.
pause
exit /b 0

:fail
echo.
echo Build FAILED.
echo.
pause
exit /b 1
