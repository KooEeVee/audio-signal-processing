import play
import plot


# TEST SIGNALS

# Read wav to array, sample rate 44.1 kHz
guzheng, fs = play.wav_to_array("847157__nanliu_music__guzheng-instrument-single-note-sound_mono.wav")
piano, _ = play.wav_to_array("847227__nanliu_music__acoustic-piano-c4-forte_mono.wav")
rooster, _ = play.wav_to_array("39923__dobroide__20070812rooster_mono.wav")
flute1_4, _ = play.wav_to_array("flute_C_1-4.wav")
flute1_8, _ = play.wav_to_array("flute_C_1-8.wav")
flute1_16, _ = play.wav_to_array("flute_C_1_16.wav")

def main():

    # Select a test signal: guzheng, piano, rooster, flute1_4, flute1_8, flute1_16
    signal = flute1_16
    
    # Play the test signal
    play.play(signal, fs)

if __name__ == "__main__":
    main()