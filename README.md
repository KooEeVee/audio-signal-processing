# Pitch detection with pYIN

## Introduction to pYIN algorithm

WIP

## Example results from the program runs

### Flute melody
Comparing synthesized flute notes pitch detection. The first example is eighth note duration and the second is sixteenth note duration. The algorithm detects both melodies well, which can be observed from the time-domain and spectrogram plots. However, the CQT plot and score transcription reveal notable timing problems when comparing the original score to the transcription based on detected pitches.

#### Flute 1/8 notes - original score
![Original score](img/flute_original_score.png)

#### Flute 1/8 notes - pitches in time-domain
![Pitches in time-domain](img/flute_1-8_time.png)

#### Flute 1/8 notes - spectrogram
![Pitches in spectrogram](img/flute_1-8_spectrogram.png)

#### Flute 1/8 notes - CQT
![Pitches in CQT](img/flute_1-8_cqt.png)

#### Flute 1/8 notes - transcription
![Transcription score](img/flute_1-8_transcription.png)

#### Flute 1/16 notes - original score
![Original score](img/flute_1-16_original_score.png)

#### Flute 1/16 notes - pitches in time-domain
![Pitches in time-domain](img/flute_1-16_time.png)

#### Flute 1/16 notes - spectrogram
![Pitches in spectrogram](img/flute_1-16_spectrogram.png)

#### Flute 1/16 notes - CQT
![Pitches in CQT](img/flute_1-16_cqt.png)

#### Flute 1/16 notes - transcription
![Transcription score](img/flute_1-16_transcription.png)


## Sources and references
- [GUZHENG - instrument- Single Note - Sound by nanliu_music License: Creative Commons 0](https://freesound.org/s/847157/)
- [Acoustic Piano C4 forte by nanliu_music License: Attribution NonCommercial 4.0](https://freesound.org/s/847227/)
- [20070812.rooster.wav by dobroide License: Attribution 4.0](https://freesound.org/s/39923/)
