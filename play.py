import sounddevice as sd
import soundfile as sf

def play(signal, fs):
    sd.play(signal, fs)
    sd.wait()

def wav_to_array(signal):
    data, fs = sf.read(signal, dtype="float32")
    return (data, fs)