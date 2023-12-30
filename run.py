import neurokit2 as nk
import numpy as np
import time
from threading import Thread
from bci import BCI
from music import Music

sampleDuration = 2
average = 0

bci = BCI(simulation = True)
music = Music()

def generateSamples():
    print("Generating samples")
    global average
    sample = bci.getSample(sampleDuration)
    power = nk.eeg_power(sample, sampling_rate=25)
    power_by_channels = power.mean(numeric_only=True, axis=0)
    average = np.mean(power_by_channels)
    print("Average: " + str(average))

while True:
    Thread(target = generateSamples).start()
    music.play(fast = average > 0.1)