import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from silero_vad import load_silero_vad, get_speech_timestamps
from pathlib import Path
import torch


class SpeechToText:

    def __init__(self, model_size="base", sample_rate=16000):

        self.sample_rate = sample_rate

        print("Loading model...")

        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.vad_model = load_silero_vad()

        print("Voice system ready")

    def record_audio(self, duration=5, filename="data/temp_audio.wav"):

        print("I am Listening....")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )

        sd.wait()

        audio = np.squeeze(audio)

        write(filename, self.sample_rate, audio)

        return filename

    def detect_speech(self, audio_path):

        audio = torch.from_numpy(np.fromfile(audio_path, dtype=np.float32))

        speech = get_speech_timestamps(
            audio, self.vad_model, sampling_rate=self.sample_rate
        )

        return len(speech) > 0

    def transcribe(self, audio_path):

        segments, _ = self.model.transcribe(audio_path)

        text = ""

        for segment in segments:
            text += segment.text

        return text.strip()
