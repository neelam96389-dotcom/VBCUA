"""
audio_utils.py
Audio loading and feature extraction utilities using Librosa and SoundFile.
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import re
import os

FILLER_WORDS = ["um", "uh", "like", "you know", "so", "actually", "basically"]


def extract_audio_features(audio_path: str, waveform_output_path: str = None) -> dict:
    """
    Extracts pause_ratio and rms_energy from an audio file.
    Optionally saves a waveform plot for the dashboard/report.
    """
    y, sr = librosa.load(audio_path, sr=None)

    rms = librosa.feature.rms(y=y)[0]
    rms_energy = float(np.mean(rms))

    silence_threshold = 0.02
    silent_frames = np.sum(rms < silence_threshold)
    pause_ratio = float(silent_frames / len(rms)) if len(rms) > 0 else 0.0

    if waveform_output_path:
        plt.figure(figsize=(10, 3))
        librosa.display.waveshow(y, sr=sr, color="#4F46E5")
        plt.title("Audio Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.tight_layout()
        os.makedirs(os.path.dirname(waveform_output_path), exist_ok=True)
        plt.savefig(waveform_output_path)
        plt.close()

    return {
        "rms_energy": round(rms_energy, 5),
        "pause_ratio": round(pause_ratio, 3),
        "waveform_path": waveform_output_path,
    }


def filler_word_ratio(transcript: str) -> float:
    """
    Computes the ratio of filler words to total words in the transcript.
    """
    words = transcript.lower().split()
    if not words:
        return 0.0

    filler_count = 0
    text = transcript.lower()
    for filler in FILLER_WORDS:
        filler_count += len(re.findall(rf"\b{re.escape(filler)}\b", text))

    return round(filler_count / len(words), 3)
