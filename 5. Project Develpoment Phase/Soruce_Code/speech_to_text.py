"""
speech_to_text.py
Integrates OpenAI Whisper to convert uploaded audio files into text transcriptions.
"""

import whisper

_model = None


def get_model(size: str = "base"):
    global _model
    if _model is None:
        _model = whisper.load_model(size)
    return _model


def speech_to_text(audio_path: str) -> str:
    """
    Transcribes an audio file (WAV/MP3) to text using Whisper.
    Returns the transcript as a plain string.
    """
    model = get_model()
    result = model.transcribe(audio_path)
    return result.get("text", "").strip()
