import play
import plot
import librosa
import numpy as np


# TEST SIGNALS

# Read wav to array, sample rate 44.1 kHz
guzheng, fs = play.wav_to_array("847157__nanliu_music__guzheng-instrument-single-note-sound_mono.wav")
piano, _ = play.wav_to_array("847227__nanliu_music__acoustic-piano-c4-forte_mono.wav")
rooster, _ = play.wav_to_array("39923__dobroide__20070812rooster_mono.wav")
flute1_4, _ = play.wav_to_array("flute_C_1-4.wav")
flute1_8, _ = play.wav_to_array("flute_C_1-8.wav")
flute1_16, _ = play.wav_to_array("flute_C_1_16.wav")

# PARAMETERS FOR PYIN ALGORITHM

# Define parameters for frames
N_ms = 40 #[ms] frame length in milliseconds
N = int(fs * N_ms / 1000) #frame length in samples
hop = N // 2 #50% hop size, overlap in frame length

#Define a range for target frequencies
min_freq = 29 #[Hz] minimum frequency for frequency range
max_freq = 4186 #[Hz] maximum frequency for frequency range

def main():

    # Select a test signal: guzheng, piano, rooster, flute1_4, flute1_8, flute1_16
    signal = rooster
    
    # Play the test signal
    play.play(signal, fs)

    # Apply pYIN to a monophonic melody signal and plot in time
    f0, voiced_flag, voiced_prob = librosa.pyin(y=signal, fmin=min_freq, fmax=max_freq, sr=fs, frame_length=N, hop_length=hop, fill_na=0)
    t_frames = np.arange(len(f0))
    t = librosa.frames_to_time(frames=t_frames, sr=fs, hop_length=hop)
    plot.plot_in_time(t, f0, "Pitches in Time pYIN")

    # Convert pitches (Hz) to note names
    note_names = librosa.hz_to_note(f0[voiced_flag])
    print(note_names)

    # Compute Short-Time-Fourier-Transform (STFT) and plot spectrogram
    D = librosa.stft(signal, n_fft=N, hop_length=hop)
    mag = np.abs(D)
    mag_db = librosa.amplitude_to_db(mag, ref=np.max)
    plot.plot_spectrogram_f0(mag_db, hop, fs, t[voiced_flag], f0[voiced_flag], "Test Signal Pitch with pYIN")

if __name__ == "__main__":
    main()