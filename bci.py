import neurokit2 as nk
from unicorn import Unicorn

'''

Model for the BCI device. Abstracts the differences between the Unicorn and the simulation.
And applies filter to the sampled data.

'''
class BCI:
    def __init__(self, simulation):
        self.simulation = simulation

    def getSample(self, duration):
        data = self.getData(duration)
        # Appply band pass fitler to 30Hz
        filtered = nk.signal_filter(data, sampling_rate = 100, lowcut=1, highcut=30)
        return filtered

    def getData(self, duration):
        return nk.eeg_simulate(duration=duration, sampling_rate=25) if self.simulation else Unicorn.getSample(duration)