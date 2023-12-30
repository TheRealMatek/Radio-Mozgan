import neurokit2 as nk
import numpy as np
import time
from mingus.midi import fluidsynth
from mingus.containers import Note, NoteContainer
from mingus.core import intervals, progressions
from random import random
from threading import Thread
import platform

# Music generation code adapted from https://medium.com/@andrewadiletta/producing-music-with-rules-python-tutorial-8c4005f276f0

soundFontPath = "./FluidR3_GM.sf2"
if platform.system() == "Linux":
    fluidsynth.init(soundFontPath, "pulseaudio")
else:
    fluidsynth.init(soundFontPath)

progression = ["iv","v7","vi","iii7", "iv", "idom7", "iv", "v"]
key = "C"
chords = progressions.to_chords(progression, key)

# Initial params
deviation = 0.5
average = 0.5
lastSampleTime = 0

def generateSamples():
    print("Generating samples")
    global deviation
    global average
    global lastSampleTime
    eeg = nk.eeg_simulate(duration=1, sampling_rate=1000, noise=0.2)
    power = nk.eeg_power(eeg, sampling_rate=500, show=False, frequency_band= ['Gamma','Beta','Alpha','Theta','Delta'])
    power_by_channels = power.mean(numeric_only=True, axis=0)
    deviation = np.std(power_by_channels) / 10
    average = np.mean(power_by_channels) / 10
    lastSampleTime = time.time()
    return average, deviation

while True:
    if lastSampleTime + 2 + random() < time.time():
        Thread(target = generateSamples).start()
    for i in range(len(chords)):
        current_chord = NoteContainer(chords[i])
        base_note = Note(current_chord[0].name)
        base_note.octave_down()
        fluidsynth.play_Note(base_note)
        time.sleep(1) 
        # Play highest note in chord
        fluidsynth.play_Note(current_chord[-1])  
        # 50% chance on a bass note
        if random() > 0.5 + average:
            second_base_note = Note(current_chord[1].name)
            second_base_note.octave_down()
            fluidsynth.play_Note(second_base_note)
        time.sleep(0.5 + deviation)       
        # 50% chance on a ninth
        if random() > 0.5 + average:
            ninth_note = Note(intervals.third(current_chord[0].name, key))
            ninth_note.octave_up()
            fluidsynth.play_Note(ninth_note)
        time.sleep(0.5 + deviation)        
        # 50% chance on a last note
        if random() > 0.5 + average:
            fluidsynth.play_Note(current_chord[-2])
        time.sleep(0.25)
