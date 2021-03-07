import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import scipy
import math
import statistics
from statistics import mode

def fft(samples,sample_rate):
    n=len(samples)
    t=1/sample_rate
    yf = scipy.fft.fft(samples)
    freq = np.linspace(0,int(1/(2*t)),int(n/2))
    mag = 2/n*np.abs(yf[:n//2])
    return mag,freq

def frequency_to_note(frequency):
    #https://stackoverflow.com/questions/64505024/turning-a-frequency-into-a-note-in-python
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    OCTAVE_MULTIPLIER = 2
    KNOWN_NOTE_NAME, KNOWN_NOTE_OCTAVE, KNOWN_NOTE_FREQUENCY = ('A', 4, 440)

    note_multiplier = OCTAVE_MULTIPLIER**(1/len(NOTES))
    frequency_relative_to_known_note = frequency / KNOWN_NOTE_FREQUENCY
    distance_from_known_note = math.log(frequency_relative_to_known_note, note_multiplier)

    distance_from_known_note = round(distance_from_known_note)

    known_note_index_in_octave = NOTES.index(KNOWN_NOTE_NAME)
    known_note_absolute_index = KNOWN_NOTE_OCTAVE * len(NOTES) + known_note_index_in_octave
    note_absolute_index = known_note_absolute_index + distance_from_known_note
    note_octave, note_index_in_octave = note_absolute_index // len(NOTES), note_absolute_index % len(NOTES)
    note_name = NOTES[note_index_in_octave]
    return (note_name, note_octave)


mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = int(1024)
stream = mic.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)


storage = []
while True:
    data = stream.read(CHUNK,exception_on_overflow = False)
    data = np.frombuffer(data, np.int16)
    sound = np.average(abs(data))

    mag,freq = fft(data,RATE)

    if sound > 20:
        index = np.argmax(mag)
        maxfreq = max(1,int(freq[index]))
        note = frequency_to_note(maxfreq)
        storage.append(note)
        if len(storage) == 5:
            try:
                print(mode(storage))
                storage = []
            except:
                storage = []

stream.stop_stream()
stream.close()
p.terminate()

#print(frames)
