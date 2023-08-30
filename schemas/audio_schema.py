from mutagen.flac import FLAC
from mutagen.mp3 import MP3
import wave
import os

def get_audio_metadata(file_path):
    audio_name = os.path.basename(file_path)
    audio_size = os.path.getsize(file_path)
    audio_sample_rate = None
    audio_bit_depth = None
    audio_duration = None

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.wav':
        with wave.open(file_path, 'rb') as audio:
            audio_sample_rate = audio.getframerate()
            audio_bit_depth = audio.getsampwidth() * 8
            audio_duration = audio.getnframes() / float(audio_sample_rate)

    elif file_extension == '.mp3':
        audio = MP3(file_path)
        audio_sample_rate = audio.info.sample_rate
        audio_duration = audio.info.length

    elif file_extension == '.flac':
        audio = FLAC(file_path)
        audio_sample_rate = audio.info.sample_rate
        audio_duration = audio.info.length

    else:
        raise ValueError("Format audio tidak didukung")

    return {
        "name": audio_name,
        "size": audio_size,
        "sample_rate": audio_sample_rate,
        "bit_depth": audio_bit_depth,
        "duration": audio_duration,
        "file_type": file_extension
    }