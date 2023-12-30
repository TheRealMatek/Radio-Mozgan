import numpy as np
from librosa import note_to_hz
import pyaudio

class Ocsilator:
    def __init__(self, frequency, amplitude, sampling_rate=44100, time=0):
        self.frequency = frequency
        self.amplitude = amplitude
        self.sampling_rate = sampling_rate
        self.time = time

    def get_sample(self):
        self.time += 1 / self.sampling_rate
        return self.value()

    def get_samples(self, duration):
        return np.array([self.get_sample() for _ in range(duration * self.sampling_rate)])
    
    def value(self):
        return False
    
class SinOscialtor(Ocsilator):
    def value(self):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * self.time)

class SquareOscialtor(Ocsilator):
    def value(self):
        return self.amplitude * np.sign(np.sin(2 * np.pi * self.frequency * self.time))
    
class SawOscialtor(Ocsilator):
    def value(self):
        return self.amplitude * (self.time * self.frequency - np.floor(self.time * self.frequency))
    
# def generateBrainWaves():
#     eeg = nk.eeg_simulate(duration=3, sampling_rate=500, noise=0.2)
#     channels = nk.eeg_power(eeg, sampling_rate=500, show=False, frequency_band=list(channel_notes.keys()))
#     average = channels.mean(numeric_only=True, axis=0)
#     return average

duration = 2
gamma = SawOscialtor(note_to_hz("C4"), 1).get_samples(duration)
beta = SawOscialtor(note_to_hz("E4"), 1).get_samples(duration)
alpha = SawOscialtor(note_to_hz("G4"), 1).get_samples(duration)
theta = SawOscialtor(note_to_hz("B4"), 1).get_samples(duration)
delta = SawOscialtor(note_to_hz("C5"), 0).get_samples(duration)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

output = np.sum([gamma, beta, alpha, theta], axis=0) / 5
stream.write(output.astype(np.float32).tobytes())
stream.close()
p.terminate()
