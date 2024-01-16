import neurokit2 as nk
# import numpy as np
# import time
# from threading import Thread
# from bci import BCI
from music import Music
from unicornhybridblack import UnicornBlackThreads, UnicornBlackProcess
from unicornhybridblack import UnicornGroomPSD, UnicornGroomFilter
import time
import numpy as np
from scipy import signal, interpolate, ndimage
from sklearn.decomposition import FastICA
import threading

sampleDuration = 1
average = 0
simulation = False
# bci = BCI(simulation = False)
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

def meanPower(freq, power):
    mean_power = {}
    wave_freqs = {
        'Alpha': [8, 13],
        'Beta': [13, 30],
        'Gamma': [30, 80],
        'Delta': [1, 4],
        'Theta': [4, 8],
    }
    for channel, freq_bounds in wave_freqs.items():
        mean_power[channel] = np.mean(power[np.where(np.logical_and(freq >= freq_bounds[0], freq <= freq_bounds[1]))])
    return mean_power

# UnicornBlack = UnicornBlackThreads() 
# UnicornBlack.logdata = False
# UnicornBlack.connect(deviceID='UN-2021.04.14', rollingspan=5, logfilename='default')
# UnicornBlack.startrecording()

# bci = BCI(simulation = False)

def preprocess(data):
    data = signal.detrend(data)
    data = np.array(UnicornGroomFilter(data, notchfilter=50), copy=True)
    # Add smoothing
    data = ndimage.gaussian_filter1d(data, sigma=1)
    data = interpolate.interp1d(np.arange(len(data)), data)(np.linspace(0, len(data) - 1, len(data)))
    return data

def peaks(data):
    max = np.max(np.sqrt(np.abs(data)))
    std = np.std(data)
    threshold = max - std/len(data)
    # print(max, std, threshold)
    return signal.find_peaks(data, prominence=60)[0]

# Example code for calling the Unicorn device as a thread
UnicornBlack = UnicornBlackThreads()   
        
# all other functions and calls remain the same    
UnicornBlack.connect(deviceID='UN-2021.04.14', rollingspan=2, logfilename='recordeddata_thread')
reference_beta = 0

music = Music()
MusicThread = threading.Thread(target=music.play)
MusicThread.start()
# music.start()
# music.play()
# MusicThread.start()

UnicornBlack.startrecording()
for i in range(10):
    time.sleep(2)
    data = np.array(UnicornBlack.sample_data())

    eegs = data[:,:8]
    means_powers = []
    for ch in range(8):
        filtered = np.array(UnicornGroomFilter(eegs[:, ch], notchfilter=50), copy=True)
        power, freqs = UnicornGroomPSD(filtered)
        means_powers.append(meanPower(freqs, power))
    
    if i == 0:
        reference_beta = np.mean([mean_power['Beta'] for mean_power in means_powers])
    else:
        beta = np.mean([mean_power['Beta'] for mean_power in means_powers])
        if beta > reference_beta:
            music.work.set()
            print("Work")
        else :
            music.work.clear()
            print("Relax")

    mid = preprocess(data[:, 0])
    left = preprocess(data[:, 1])
    right = preprocess(data[:, 2])

    mid_peaks = peaks(mid)
    left_peaks = peaks(left)
    right_peaks = peaks(right)

    left_detection = len(left_peaks) > 0
    right_detection = len(right_peaks) > 0
    mid_detection = len(mid_peaks) > 0

    if left_detection + right_detection + mid_detection > 1:
        music.blink.set()
        print("Blink detected")
    else:
        music.blink.clear()
        print("No blink detected")
    # print("Mid peaks", mid_peaks)
    # print("Left peaks", left_peaks)
    # print("Right peaks", right_peaks)
    # # if len(left_peaks) > 0:
        # print("Blink detected")
    # for channel in range(8):
    #     example = np.array(UnicornGroomFilter(data, notchfilter=50), copy=True)
    # print("Blink count", len(left_peaks), len(right_peaks))
music.stop.set()
UnicornBlack.disconnect()

# while True:
#     sample = bci.getSample(5)
#     sample = np.swapaxes(sample, 0, 1)
#     print(sample.shape)
#     print(sample[0])
#     print(np.max(sample[:2]))
    # music.play(fast = average > 0.017)
    # if not UnicornBlack.ready:
    #     continue
    # sample = np.array(UnicornBlack.sample_data(), copy=True)
    # sample = np.swapaxes(sample, 0, 1)
    # print(sample[0])
    # sample = sample[:8]

    # _power, _freqs = UnicornGroomPSD(sample)
    # band_power = meanPower(_freqs, _power)

    # print(np.max(sample[:2]))

    # ibi = np.abs((band_power['Delta'] + band_power['Theta']) - band_power['Gamma'])
    # print(ibi)

    # ica = FastICA(n_components=2)

    # print(ica.fit_transform(sample))

    
    # power = nk.eeg_power(example, frequency_band=['Alpha', 'Beta', 'Gamma', 'Theta', 'Delta'])
    # band_power = power.mean(numeric_only=True, axis=0)
    # print("______")
    # print(ibi)
    # print(band_power['Alpha'])
    # print(band_power['Beta'])
    # print(alpha)
    # print(beta)
    # print(np.abs(alpha - beta))
    # if alpha > 115 :
    #     print("Relaxed")
    # if (np.abs(band_power['Alpha'] - band_power['Beta']) > 0.01):
    #     music.play(fast = True)
    # if band_power['Beta'] > 0.0015:
    #     music.play(fast = True)
    # time.sleep(0.3)