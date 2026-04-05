import matplotlib.pyplot as plt
import librosa.display
import numpy as np

# Plot signal in time-domain
def plot_in_time(t, x, title):
    plt.figure()
    plt.plot(t, x)
    plt.title(f"{title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

# Plot signal spectrogram in seconds and frequencies and detected pitch
def plot_spectrogram_f0(mag_db, hop, fs, t, f0, title):
    plt.figure()
    img = plt.imshow(mag_db, origin="lower", aspect="auto", cmap="binary", extent=[0, mag_db.shape[1] * hop / fs, 0, fs / 2])
    plt.plot(t, f0, color="red", linewidth=1, label="Pitch Estimation")
    plt.ylim(0, 5000)
    plt.title(f"Spectrogram: {title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.legend()
    plt.colorbar(img, label="Magnitude [dB]")
    plt.show()

# Plot signal CQT in seconds and note names and detected pitch with note names
def plot_cqt_f0_notes(mag_db, hop, fs, t, f0, bins, f_min, onset_times, note_names, onset_pitches, title):
    plt.figure()
    img = librosa.display.specshow(mag_db, sr=fs, x_axis="time", y_axis="cqt_note", bins_per_octave=bins, fmin=f_min, hop_length=hop, cmap="binary")
    plt.plot(t, f0, color="lime", linewidth=1, label="Pitch Estimation")
    for onset, note, pitch_hz in zip(onset_times, note_names, onset_pitches):
        plt.text(onset, pitch_hz + 20, note, color="lime", fontsize=12, ha="center", va="bottom")
    plt.title(f"Constant_Q Transform: {title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Note")
    plt.legend()
    plt.colorbar(img, label="Magnitude [dB]")
    plt.show()