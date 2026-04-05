# Pitch detection with pYIN

## Introduction to pYIN algorithm

WIP

## Implementation

The program is implemented in Python using the following libraries:
- librosa — pYIN pitch detection, STFT, CQT, onset detection
- pretty_midi — MIDI file creation and export
- music21 — MusicXML file generation from MIDI
- sounddevice / soundfile — audio playback and WAV file loading
- matplotlib.pyplot — visualization
- numpy — array and numerical processing

### Test signals
All signals are mono WAV files sampled at 44.1 kHz (fs = 44100 Hz). Signals are loaded as float32 numpy arrays.
- guzheng - single notes recorded from a traditional Chinese string instrument (notes: A3, C3)
- piano - single note recorded from an acoustic piano (note: C4)
- rooster - recorded rooster crow, non-musical test case
- flute1_4  - synthesized flute notes, quarter note duration, tempo 120bpm (notes: C5, D5, E5, F5, G4, A4, B4, C5)
- flute1_8  - synthesized flute notes, eighth note duration, tempo 120bpm (notes: C5, D5, E5, F5, G4, A4, B4, C5)
- flute1_16 - synthesized flute notes, sixteenth note duration, tempo 120bpm (notes: C5, D5, E5, F5, G4, A4, B4, C5)

### pYIN parameters
- N_ms - frame length in milliseconds
- N - frame length converted to samples
- hop - hop size in samples
- min_freq - minimum frequency for pYIN search range in Hz (29 Hz ≈ A0, lowest piano key)
- max_freq - maximum frequency for pYIN search range in Hz (4186 Hz ≈ C8, highest piano key)

### Select and play a test signal
Select the signal from the available test signals. Play the signal through the default audio output device.

### Apply pYIN algorithm to estimate fundamental frequency (F0) of the signal and plot pitches in time-domain
- f0 - F0 estimate in Hz per frame, 0 where unvoiced
- voiced_flag - boolean array, True where the frame is classified as voiced
- voiced_prob - probability of each frame being voiced [0, 1]
- t_frames and t convert frame indices to time in seconds for plotting

### Convert F0 estimates from Hz to note names (e.g. "C4", "A3")
Only voiced frames are converted, unvoiced frames are excluded via voiced_flag.

### Compute Short-Time Fourier Transform (STFT) and plot spectrogram with F0 overlay
The spectrogram is plotted with the pYIN F0 estimate overlaid in red, showing only voiced frames.
- D - complex STFT matrix
- mag - magnitude spectrum, absolute values of D
- mag_db - magnitude converted to decibels, normalized to the peak magnitude

### Compute Constant-Q Transform (CQT) covering the full piano range
The CQT uses logarithmically spaced frequency bins. Well suited for musical pitch analysis where notes are equally spaced on a log scale.
- f_min - minimum frequency, A0 (27.5 Hz), the lowest note on a piano
- bins - total number of frequency bins, 88 covering the full piano range
- bins_octave - frequency resolution, 12 bins per octave (one bin per semitone)
- C - complex CQT matrix
- mag - magnitude spectrum, absolute values of C
- mag_db - magnitude converted to decibels, normalized to the peak magnitude

### Detect note onsets in the signal
Merge onsets that are closer together than the threshold. This prevents a single note from being split into multiple segments due to transient artifacts or vibrato.

### Segment the signal by onset times and estimate the pitch of each segment
Each segment spans from one onset to the next, with the last segment ending at the end of the signal. Each note is stored as a tuple: (midi_note, start_time, end_time, median_pitch).
- frame_times - time in seconds for each pYIN frame
- signal_end - total duration of the signal in seconds
- mask - boolean array selecting frames within the current segment that are also voiced, used to extract pitched frames only
- segment_pitches - F0 values in Hz for all voiced frames in the segment
- median_pitch  - median F0 of the segment
- midi_note_pyin - segment pitch rounded to the nearest MIDI note number

### Merge consecutive segments with the same MIDI note into a single note
If two consecutive segments have the same MIDI note: end time is extended to the later of the two end times, median pitch is averaged between the two segments. If the MIDI note changes, the segment is appended as a new note.
- clean_notes - deduplicated list of notes, each as (midi_note, start_time, end_time, median_pitch)
- last_midi - tracks the previous MIDI note to detect consecutive duplicates

### Extract note names, onset times and pitches for plotting
MIDI note numbers are converted to note name strings (e.g. 60 -> "C4"). The CQT spectrogram is plotted with the pYIN F0 estimate overlaid in green and note name labels at each onset position.
- note_names_unique - note name strings for each unique note (e.g. "C4", "A3")
- onset_times_unique - start time in seconds for each unique note
- onset_pitches - median pitch in Hz for each unique note

### Export detected notes to a MIDI file
A single piano instrument is created and all clean_notes are added as MIDI notes. The MIDI file is saved as notes_pyin.mid in the project directory.
- velocity - note loudness, fixed at 100 (range 0-127)
- pitch - MIDI note number
- start - note onset time in seconds
- end - note offset time in seconds

### Convert the MIDI file to MusicXML
- MusicXML is a standard notation format readable by notation software such as MuseScore. The MusicXML file is saved as notes_pyin.xml in the project directory.

## Sources and references
- [GUZHENG - instrument- Single Note - Sound by nanliu_music License: Creative Commons 0](https://freesound.org/s/847157/)
- [Acoustic Piano C4 forte by nanliu_music License: Attribution NonCommercial 4.0](https://freesound.org/s/847227/)
- [20070812.rooster.wav by dobroide License: Attribution 4.0](https://freesound.org/s/39923/)
