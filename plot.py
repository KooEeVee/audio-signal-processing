import matplotlib.pyplot as plt
import librosa.display
import numpy as np

# Plot signal in time-domain
def plot_in_time(t, x, voiced_prob, original, fs):
    t_signal = np.arange(len(original)) / fs
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    ax1.plot(t, x)
    ax1.set_title("f0 Estimations")
    ax1.set_ylabel("Frequency [Hz]")
    ax1.grid(True)
    ax2.plot(t, voiced_prob, color="orange")
    ax2.set_title("Voiced Probabilities")
    ax2.set_ylabel("Voiced Probability")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylim(0, 1)
    ax2.grid(True)
    ax3.plot(t_signal, original, color="green")
    ax3.set_title("Original Signal")
    ax3.set_ylabel("Amplitude")
    ax3.set_xlabel("Time [s]")
    ax3.grid(True)
    plt.tight_layout()
    plt.show()

# Plot signal spectrogram in seconds and frequencies and detected pitch with frequencies
def plot_spectrogram_f0(mag_db, hop, fs, t, f0, title):
    plt.figure()
    img = plt.imshow(mag_db, origin="lower", aspect="auto", cmap="binary", extent=[0, mag_db.shape[1] * hop / fs, 0, fs / 2])
    plt.plot(t, f0, color="red", linewidth=3, label="Pitch Estimation")
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
    plt.plot(t, f0, color="lime", linewidth=3, label="Pitch Estimation")
    for onset, note, pitch_hz in zip(onset_times, note_names, onset_pitches):
        plt.text(onset, pitch_hz + 20, note, color="lime", fontsize=12, ha="center", va="bottom")
    plt.title(f"Constant_Q Transform: {title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Note")
    plt.legend()
    plt.colorbar(img, label="Magnitude [dB]")
    plt.show()

# Plot signal CQT in seconds and frequencies and detected pitch with frequencies
def plot_cqt_f0_hz(mag_db, hop, fs, t, f0, bins, f_min, onset_times, hz, onset_pitches, title):
    plt.figure()
    img = librosa.display.specshow(mag_db, sr=fs, x_axis="time", y_axis="cqt_hz", bins_per_octave=bins, fmin=f_min, hop_length=hop, cmap="binary")
    plt.plot(t, f0, color="lime", linewidth=3, label="Pitch Estimation")
    for onset, note, pitch_hz in zip(onset_times, hz, onset_pitches):
        plt.text(onset, pitch_hz + 20, note, color="lime", fontsize=12, ha="center", va="bottom")
    plt.title(f"Constant_Q Transform: {title}")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.legend()
    plt.colorbar(img, label="Magnitude [dB]")
    plt.show()