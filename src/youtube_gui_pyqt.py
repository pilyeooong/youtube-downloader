import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, 
                           QFileDialog, QRadioButton, QButtonGroup, QProgressBar,
                           QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import yt_dlp
import os

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, url, output_path, quality):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.quality = quality
    
    def run(self):
        try:
            self.progress_signal.emit(f"다운로드 시작: {self.url}")
            
            if self.quality == "bestaudio[ext=m4a]":
                ydl_opts = {
                    'format': self.quality,
                    'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            else:
                ydl_opts = {
                    'format': self.quality,
                    'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                }
            
            class MyLogger:
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
            
            ydl_opts['logger'] = MyLogger(self)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            self.finished_signal.emit(True, "다운로드 완료!")
            
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
            0: 'best',
            1: 'best[height<=720]',
            2: 'best[height<=480]',
            3: 'bestaudio[ext=m4a]'
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
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()