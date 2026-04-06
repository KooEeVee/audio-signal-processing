import play
import plot
import librosa
import numpy as np
import pretty_midi
from music21 import converter

# TEST SIGNALS

# Read wav to array, sample rate 44.1 kHz
guzheng, fs = play.wav_to_array("847157__nanliu_music__guzheng-instrument-single-note-sound_mono.wav")
piano, _ = play.wav_to_array("847227__nanliu_music__acoustic-piano-c4-forte_mono.wav")
rooster, _ = play.wav_to_array("39923__dobroide__20070812rooster_mono.wav")
flute1_4, _ = play.wav_to_array("flute_C_1-4.wav")
flute1_8, _ = play.wav_to_array("flute_C_1-8.wav")
flute1_16, _ = play.wav_to_array("flute_C_1_16.wav")
#piano_A7, _ = play.wav_to_array("Piano.ff.A7.44100.wav")
#male_voice, _ = play.wav_to_array("MI49_07.wav")
#female_voice, _ = play.wav_to_array("FD19_04.wav")

# PARAMETERS FOR PYIN ALGORITHM

#-----------------------------------------------------------------------------#
# Define parameters for frames
N_ms = 40 #[ms] frame length in milliseconds <-- adjust this parameter
N = int(fs * N_ms / 1000) #frame length in samples
hop = N // 2 #50% hop size, overlap in frame length

#Define a range for target frequencies
min_freq = 29 #[Hz] minimum frequency for frequency range <-- adjust this parameter
max_freq = 4186 #[Hz] maximum frequency for frequency range <-- adjust this parameter
#-----------------------------------------------------------------------------#

def main():

    # SELECT AND PLAY A TEST SIGNAL

    #-----------------------------------------------------------------------------#
    # Select a test signal: guzheng, piano, rooster, flute1_4, flute1_8, flute1_16, piano_A7
    signal = flute1_16
    #-----------------------------------------------------------------------------#
    
    # Play the test signal
    play.play(signal, fs)

    # PYIN COMPUTATION AND PLOTTING IN TIME-DOMAIN

    # Apply pYIN to a monophonic melody signal and plot in time
    f0, voiced_flag, voiced_prob = librosa.pyin(y=signal, fmin=min_freq, fmax=max_freq, sr=fs, frame_length=N, hop_length=hop, fill_na=0)
    t_frames = np.arange(len(f0))
    t = librosa.frames_to_time(frames=t_frames, sr=fs, hop_length=hop)
    plot.plot_in_time(t, f0, "Pitches in Time pYIN")

    # Convert pitches (Hz) to note names
    note_names = librosa.hz_to_note(f0[voiced_flag])
    print(note_names)

    # STFT COMPUTATION AND PLOTTING A SPECTROGRAM

    # Compute Short-Time-Fourier-Transform (STFT) and plot spectrogram
    D = librosa.stft(signal, n_fft=N, hop_length=hop)
    mag = np.abs(D)
    mag_db = librosa.amplitude_to_db(mag, ref=np.max)
    plot.plot_spectrogram_f0(mag_db, hop, fs, t[voiced_flag], f0[voiced_flag], "Test Signal Pitch with pYIN")

    # CQT COMPUTATION

    # Compute Constant-Q Transform (CQT)
    f_min = librosa.note_to_hz("A0")
    bins = 88
    bins_octave = 12
    C = librosa.cqt(signal, sr=fs, hop_length=hop, fmin=f_min, n_bins=bins, bins_per_octave=bins_octave)
    mag = np.abs(C)
    mag_db = librosa.amplitude_to_db(mag, ref=np.max)

    # DETECTING THE NOTES ONSETS AND MEDIAN PITCHES

    # Detect note onset and merge by median pitch
    onset_frames = librosa.onset.onset_detect(y=signal, sr=fs, hop_length=hop) #frame indices where onsets are detected
    onset_times = librosa.frames_to_time(onset_frames, sr=fs, hop_length=hop) #onset positions converted to seconds

    if len(onset_times) == 0:
        print("No onsets detected.")

    else:
        #-----------------------------------------------------------------------------#
        #Onset merging threshold
        threshold = 0.1 #[s] threshold in seconds <-- adjust this parameter: lower for faster note changes
        #-----------------------------------------------------------------------------#

        merged = [onset_times[0]]
        for onset in onset_times[1:]:
            if onset - merged[-1] >= threshold:
                merged.append(onset)
        onset_times = merged

        notes = []
        signal_end = librosa.get_duration(y=signal, sr=fs)
        frame_times = librosa.frames_to_time(np.arange(len(f0)), sr=fs, hop_length=hop)
        for i, start_time in enumerate(onset_times):
            end_time = onset_times[i + 1] if i + 1 < len(onset_times) else signal_end
            mask = (frame_times >= start_time) & (frame_times < end_time) & (voiced_flag)
            segment_pitches = f0[mask]

            if len(segment_pitches) == 0:
                continue
            
            median_pitch = np.median(segment_pitches)
            midi_note_pyin = int(np.round(librosa.hz_to_midi(median_pitch)))
            notes.append((midi_note_pyin, start_time, end_time, median_pitch))

        clean_notes = []
        last_midi = None

        for midi_note, start_time, end_time, median_pitch in notes:
            if midi_note != last_midi:
                clean_notes.append((midi_note, start_time, end_time, median_pitch))
                last_midi = midi_note
            else:
                previous = clean_notes[-1]
                merged_end_time = max(previous[2], end_time)
                merged_pitch = (previous[3] + median_pitch) / 2
                clean_notes[-1] = (previous[0], previous[1], merged_end_time, merged_pitch)

        note_names_unique = []
        onset_times_unique = []
        onset_pitches = []
        onset_pitches_hz = []

        for midi_note, start_time, end_time, median_pitch in clean_notes:
            note_name = librosa.midi_to_note(midi_note)
            note_names_unique.append(note_name)
            onset_times_unique.append(start_time)
            onset_pitches.append(median_pitch)
            onset_pitches_hz.append(f"{median_pitch:.1f}")

        #print(f"Onset times: {onset_times_unique}")
        #print(f"Onset pitches: {onset_pitches}")
        plot.plot_cqt_f0_notes(mag_db, hop, fs, t[voiced_flag], f0[voiced_flag], bins_octave, f_min, onset_times_unique, note_names_unique, onset_pitches, "Test Signal Pitch with pYIN")
        plot.plot_cqt_f0_hz(mag_db, hop, fs, t[voiced_flag], f0[voiced_flag], bins_octave, f_min, onset_times_unique, onset_pitches_hz, onset_pitches, "Test Signal Pitch with pYIN")

"""         # TRANSCRIPTING THE NOTES TO A SCORE FILE

        # Save MIDI note as MIDI file
        midi = pretty_midi.PrettyMIDI()
        piano = pretty_midi.Instrument(program=0)
        for pitch, start, end, _ in clean_notes:
            note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
            piano.notes.append(note)
        midi.instruments.append(piano)
        midi.write("notes_pyin.mid")

        # Generate MusicXML file using MIDI file
        score = converter.parse("notes_pyin.mid")
        score.write("musicxml", fp="notes_pyin.xml") """

if __name__ == "__main__":
    main()