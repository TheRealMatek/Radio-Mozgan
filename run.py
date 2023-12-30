import neurokit2 as nk
import numpy as np
import time
from mingus.midi import fluidsynth
from mingus.containers import Note, NoteContainer
from mingus.core import intervals, progressions
from random import random
from threading import Thread
import platform
from Unicorn import Unicorn

# Music generation code adapted from https://medium.com/@andrewadiletta/producing-music-with-rules-python-tutorial-8c4005f276f0

soundFontPath = "./FluidR3_GM.sf2"
simulation = False

if platform.system() == "Linux":
    fluidsynth.init(soundFontPath, "pulseaudio")
else:
    fluidsynth.init(soundFontPath)

progression = ["iv","v7","vi","iii7", "iv", "idom7", "iv", "v"]
key = "C"
chords = progressions.to_chords(progression, key)

sampleDuration = 2
averageCutoff = 2

# Initial params
deviation = 0
average = 0
lastSampleTime = 0

def generateSamples():
    print("Generating samples")
    if simulation:
        eeg = nk.eeg_simulate(duration=1, sampling_rate=25)
    else:
        eeg = Unicorn().getSample(sampleDuration)

    filtered = nk.signal_filter(eeg, sampling_rate = 100, lowcut=1, highcut=30)
    power = nk.eeg_power(filtered, sampling_rate=100, show=False, frequency_band=['Gamma','Beta','Alpha','Theta','Delta'])
    power_by_channels = power.mean(numeric_only=True, axis=0)
    deviation = np.std(power_by_channels)
    average = np.mean(power_by_channels)
    return average, deviation

def playMusic():
    global average
    global averageCutoff
    while True:
        for i in range(len(chords)):
            current_chord = NoteContainer(chords[i])
            base_note = Note(current_chord[0].name)
            base_note.octave_down()
            fluidsynth.play_Note(base_note)
            time.sleep(1) 
            # Play highest note in chord
            fluidsynth.play_Note(current_chord[-1])  
            # 50% chance on a bass note
            if average > averageCutoff:
                second_base_note = Note(current_chord[1].name)
                second_base_note.octave_down()
                fluidsynth.play_Note(second_base_note)
            time.sleep(0.5)       
            # 50% chance on a ninth
            if average > averageCutoff:
                ninth_note = Note(intervals.third(current_chord[0].name, key))
                ninth_note.octave_up()
                fluidsynth.play_Note(ninth_note)
            time.sleep(0.5)     
            # 50% chance on a last note
            if average > averageCutoff:
                fluidsynth.play_Note(current_chord[-2])
            time.sleep(0.25)

Thread(target=playMusic).start()
while True:
    if lastSampleTime + sampleDuration < time.time():
        average, deviation = generateSamples()
        print(average)
        lastSampleTime = time.time()
        # Thread(target = generateSamples).start()