import neurokit2 as nk
import numpy as np

'''

Model for the BCI device. Abstracts the differences between the Unicorn and the simulation.
And applies filter to the sampled data.

'''
class BCI:
    def __init__(self, simulation):
        self.simulation = simulation
        if not simulation:
            self.unicorn = Unicorn()

    def getSample(self, duration):
        data = self.getData(duration)
        return data

    def getData(self, duration):
        if self.simulation:
            return nk.eeg_simulate(duration=duration, sampling_rate=250)
        else:
            UnicornBlack = UnicornBlackThreads() 
            UnicornBlack.connect(deviceID='UN-2021.04.14', rollingspan=3.0, logfilename='default')
            print('Battery: %0.1f%%' % UnicornBlack.check_battery())
            UnicornBlack.startrecording()
            duration = 10
            for incrX in range(duration):
                    time.sleep(1)
                    UnicornBlack.safe_to_log(False)
                    UnicornBlack.mark_event(incrX)
                    print("Time Lapsed: %d second" % (incrX+1))
                    UnicornBlack.safe_to_log(True)
        return 