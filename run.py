import neurokit2 as nk
# import numpy as np
# import time
# from threading import Thread
# from bci import BCI
from music import Music
from unicornhybridblack import UnicornBlackThreads
import time
import numpy as np
from scipy import signal

sampleDuration = 1
average = 0
simulation = False
# bci = BCI(simulation = False)
music = Music()

# def generateSamples():
#     print("Generating samples")
#     global average
#     sample = bci.getSample(sampleDuration)
#     print("Sampled")
#     if sample is None:
#         return
#     power = nk.eeg_power(sample, sampling_rate=50, frequency_band=['Alpha', 'Beta'])
#     power_by_channels = power.mean(numeric_only=True, axis=0)
#     std = power_by_channels.std()
#     print("Standard deviation", std)
#     print("Power by channels", power_by_channels)
#     average = power_by_channels['Beta']

UnicornBlack = UnicornBlackThreads() 
UnicornBlack.logdata = False
UnicornBlack.connect(deviceID='UN-2021.04.14', rollingspan=3.0, logfilename='default')
UnicornBlack.startrecording()
while True:
    music.play(fast = average > 0.017)
    if not UnicornBlack.ready:
        continue
    example = UnicornBlack.data
    example = np.swapaxes(example, 0, 1)
    example = example[:8]
    power = nk.eeg_power(example, sampling_rate=250, frequency_band=['Alpha', 'Beta'])
    band_power = power.mean(numeric_only=True, axis=0)
    print(band_power['Alpha'])
    print(band_power['Beta'])