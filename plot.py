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