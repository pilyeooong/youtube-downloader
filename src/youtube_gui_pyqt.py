import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                           QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                           QFileDialog, QRadioButton, QButtonGroup, QProgressBar,
                           QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import yt_dlp
import os
import shutil

def setup_bundled_binaries():
    """번들된 바이너리(ffmpeg, deno 등)를 PATH에 추가"""
    if not getattr(sys, 'frozen', False):
        return
    base_path = sys._MEIPASS
    # 번들 경로를 PATH 맨 앞에 추가하면 ffmpeg, deno 모두 자동 인식
    os.environ['PATH'] = base_path + os.pathsep + os.environ.get('PATH', '')

def get_ffmpeg_path():
    """번들된 ffmpeg 경로 또는 시스템 ffmpeg 반환"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        # Windows 번들 바이너리는 ffmpeg.exe다. 확장자를 빼면 항상 탐지에 실패한다.
        suffix = '.exe' if sys.platform == 'win32' else ''
        if os.path.exists(os.path.join(base_path, 'ffmpeg' + suffix)):
            return base_path
    return None

def find_js_runtimes():
    """설치된 JS 런타임 탐색.

    yt-dlp 2025.11부터 YouTube는 JS 챌린지 해결을 위해 외부 런타임을 요구한다.
    bun은 2026.06.09에 지원 중단 예정으로 표시돼 제외한다.
    """
    runtimes = {}
    for rt in ('deno', 'node'):
        if shutil.which(rt):
            runtimes[rt] = {}
    return runtimes

# yt-dlp 기본 클라이언트는 ('android_vr', 'web_safari') 다.
# 403은 영상·클라이언트 조합에 따라 갈리므로(주로 GVS PO Token 요구) 다른 클라이언트로
# 바꾸면 풀리는 경우가 많다.
#
# 아래 순서는 추측이 아니라 2026-08-17 실측으로 정했다 (4K 영상 / 2005년 영상):
#   client         포맷수/최고화질            판정
#   <기본>          37 / 2160p , 11 / 240p    -
#   web_embedded   31 / 2160p , 15 / 240p    화질 보존 — 1순위
#   tv_simply       5 /  360p ,  1 / 240p    화질 저하되나 동작 — 차선
#   mweb            5 /  360p ,  1 / 240p    tv_simply 와 동급, 다른 경로로 한 번 더
#   tv              5 /  360p , DRM 오류      구영상에서 실패 → 제외
#   ios            포맷 없음   , 추출 실패     양쪽 다 실패 → 제외
# 로그인이 필요한 tv_downgraded·web_creator 도 제외.
#
# YouTube 사정에 따라 위 수치는 변한다. 폴백이 잘 안 들으면 이 표부터 다시 측정할 것.
FALLBACK_PLAYER_CLIENTS = ('web_embedded', 'tv_simply', 'mweb')

# 기본만큼의 화질이 안 나오는 클라이언트. 이걸로 받았으면 사용자에게 알린다.
_LOW_QUALITY_CLIENTS = ('tv_simply', 'mweb')

# 클라이언트를 바꾸면 복구될 수 있는 실패 신호.
# 'Requested format is not available' 은 PO Token 때문에 포맷이 통째로 스킵된 결과다.
_CLIENT_RETRY_SIGNS = (
    'http error 403',
    'forbidden',
    'po token',
    'requested format is not available',
)

def is_client_retryable(error):
    """player_client 를 바꿔 재시도할 가치가 있는 오류인지 판별."""
    msg = str(error).lower()
    return any(sign in msg for sign in _CLIENT_RETRY_SIGNS)

class _ThreadLogger:
    """yt-dlp 로그를 GUI 상태창으로 넘긴다."""

    def __init__(self, thread):
        self.thread = thread

    def debug(self, msg):
        pass

    def info(self, msg):
        self.thread.progress_signal.emit(f"정보: {msg}")

    def warning(self, msg):
        self.thread.progress_signal.emit(f"경고: {msg}")

    def error(self, msg):
        self.thread.progress_signal.emit(f"오류: {msg}")

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, url, output_path, quality):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.quality = quality
    
    def build_opts(self, js_runtimes, player_client=None):
        """ydl 옵션 구성. player_client 를 주면 그 클라이언트만 강제한다."""
        ydl_opts = {
            'format': self.quality,
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'remote_components': ['ejs:github'],
            'postprocessor_args': {'merger': ['-c:a', 'aac']},
            'js_runtimes': js_runtimes,
            'logger': _ThreadLogger(self),
        }

        if player_client:
            ydl_opts['extractor_args'] = {'youtube': {'player_client': [player_client]}}

        # 번들된 ffmpeg 경로 설정
        ffmpeg_path = get_ffmpeg_path()
        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path

        if self.quality == "bestaudio[ext=m4a]/bestaudio":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        return ydl_opts

    def run(self):
        try:
            self.progress_signal.emit(f"다운로드 시작: {self.url}")

            js_runtimes = find_js_runtimes()
            if not js_runtimes:
                self.finished_signal.emit(
                    False,
                    "JS 런타임을 찾을 수 없습니다.\n\n"
                    "YouTube 다운로드에는 deno 또는 node가 필요합니다.\n"
                    "https://deno.com 에서 설치한 뒤 다시 시도하세요.",
                )
                return

            # 첫 시도는 yt-dlp 기본 클라이언트, 403 계열이면 클라이언트를 바꿔가며 재시도한다.
            attempts = (None, *FALLBACK_PLAYER_CLIENTS)
            last_error = None

            for index, player_client in enumerate(attempts):
                if player_client:
                    self.progress_signal.emit(
                        f"403 계열 오류로 실패 — player_client '{player_client}' 로 재시도합니다 "
                        f"({index}/{len(FALLBACK_PLAYER_CLIENTS)})",
                    )

                try:
                    with yt_dlp.YoutubeDL(self.build_opts(js_runtimes, player_client)) as ydl:
                        ydl.download([self.url])
                except Exception as e:
                    # 클라이언트를 바꿔도 소용없는 오류(비공개·삭제·네트워크 등)는 즉시 중단한다.
                    if not is_client_retryable(e):
                        raise
                    last_error = e
                    continue

                done = "다운로드 완료!"
                if player_client:
                    done += f"\n\n기본 경로가 막혀 '{player_client}' 로 받았습니다."
                    if player_client in _LOW_QUALITY_CLIENTS:
                        done += ("\n이 경로는 낮은 화질(최대 360p)만 제공합니다.\n"
                                 "고화질이 필요하면 잠시 후 다시 시도해 보세요.")
                self.finished_signal.emit(True, done)
                return

            self.finished_signal.emit(
                False,
                "403 오류로 다운로드하지 못했습니다.\n"
                f"기본 클라이언트와 {', '.join(FALLBACK_PLAYER_CLIENTS)} 를 모두 시도했습니다.\n\n"
                "VPN을 쓰고 있다면 끄고, 잠시 후 다시 시도해 보세요.\n\n"
                f"마지막 오류: {last_error}",
            )

        except Exception as e:
            self.finished_signal.emit(False, f"오류 발생: {str(e)}")

class YouTubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_path = os.path.expanduser("~/Downloads")
        self.download_thread = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('YouTube 다운로더')
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # URL 입력
        url_label = QLabel('YouTube URL:')
        url_label.setFont(QFont('Arial', 12))
        layout.addWidget(url_label)
        
        self.url_input = QLineEdit()
        self.url_input.setFont(QFont('Arial', 10))
        layout.addWidget(self.url_input)
        
        # 저장 경로
        path_layout = QHBoxLayout()
        path_label = QLabel('저장 경로:')
        path_label.setFont(QFont('Arial', 10))
        path_layout.addWidget(path_label)
        
        self.path_input = QLineEdit(self.download_path)
        self.path_input.setFont(QFont('Arial', 9))
        path_layout.addWidget(self.path_input)
        
        path_btn = QPushButton('찾아보기')
        path_btn.clicked.connect(self.select_path)
        path_layout.addWidget(path_btn)
        
        layout.addLayout(path_layout)
        
        # 품질 선택
        quality_layout = QHBoxLayout()
        quality_label = QLabel('품질:')
        quality_label.setFont(QFont('Arial', 10))
        quality_layout.addWidget(quality_label)
        
        self.quality_group = QButtonGroup()
        
        self.best_radio = QRadioButton('최고 품질')
        self.best_radio.setChecked(True)
        self.quality_group.addButton(self.best_radio, 0)
        quality_layout.addWidget(self.best_radio)
        
        self.hd720_radio = QRadioButton('720p')
        self.quality_group.addButton(self.hd720_radio, 1)
        quality_layout.addWidget(self.hd720_radio)
        
        self.sd480_radio = QRadioButton('480p')
        self.quality_group.addButton(self.sd480_radio, 2)
        quality_layout.addWidget(self.sd480_radio)
        
        self.mp3_radio = QRadioButton('MP3 음성만')
        self.quality_group.addButton(self.mp3_radio, 3)
        quality_layout.addWidget(self.mp3_radio)
        
        layout.addLayout(quality_layout)
        
        # 다운로드 버튼
        self.download_btn = QPushButton('다운로드')
        self.download_btn.setFont(QFont('Arial', 12))
        self.download_btn.setStyleSheet('QPushButton { background-color: #4CAF50; color: white; padding: 10px; }')
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)
        
        # 진행률 바
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # 상태 텍스트
        self.status_text = QTextEdit()
        self.status_text.setFont(QFont('Arial', 9))
        layout.addWidget(self.status_text)
    
    def select_path(self):
        path = QFileDialog.getExistingDirectory(self, '저장 경로 선택', self.download_path)
        if path:
            self.download_path = path
            self.path_input.setText(path)
    
    def get_selected_quality(self):
        quality_map = {
            0: 'bestvideo*+bestaudio/best',
            1: 'bestvideo*[height<=720]+bestaudio/best[height<=720]',
            2: 'bestvideo*[height<=480]+bestaudio/best[height<=480]',
            3: 'bestaudio[ext=m4a]/bestaudio'
        }
        return quality_map[self.quality_group.checkedId()]
    
    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '오류', 'YouTube URL을 입력해주세요.')
            return
        
        self.download_btn.setEnabled(False)
        self.progress_bar.setRange(0, 0)  # 무한 진행
        self.status_text.clear()
        
        output_path = self.path_input.text()
        quality = self.get_selected_quality()
        
        self.download_thread = DownloadThread(url, output_path, quality)
        self.download_thread.progress_signal.connect(self.update_status)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
    
    def update_status(self, message):
        self.status_text.append(message)
    
    def download_finished(self, success, message):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.download_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, '완료', message)
        else:
            QMessageBox.critical(self, '오류', message)
        
        self.update_status(message)

def main():
    setup_bundled_binaries()
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()