from moviepy.editor import *

def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

VIDEO_FILE_PATH = "./test.mp4"
AUDIO_FILE_PATH = "./test.mp3"

MP4ToMP3(VIDEO_FILE_PATH, AUDIO_FILE_PATH)