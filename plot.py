import matplotlib.pyplot as plt
import librosa.display
import numpy as np

# Plot signal in time-domain
def plot_in_time(t, x, title):
    plt.plot(t, x)
    plt.title(f"{title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.grid(True)
    plt.show()

# Plot signal spectrogram in seconds and frequencies and detected pitch
def plot_spectrogram_f0(mag_db, hop, fs, t, f0, title):
    plt.imshow(mag_db, origin="lower", aspect="auto", cmap="binary", extent=[0, mag_db.shape[1] * hop / fs, 0, fs / 2])
    plt.plot(t, f0, color="red", linewidth=1, label="Pitch Estimation")
    plt.legend()
    plt.title(f"Spectrogram: {title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.ylim(0, 5000)
    plt.colorbar(label="Magnitude [dB]")
    plt.show()