import UnicornPy
import numpy as np

class Unicorn:
    def __init__(self):
        deviceList = UnicornPy.GetAvailableDevices(True)
        if len(deviceList) <= 0 or deviceList is None:
            raise Exception("No device available.Please pair with a Unicorn first.")
        self.device = UnicornPy.Unicorn(deviceList[0])

    def getSample(self, duration):
        frameLength = 1
        self.device.StartAcquisition(True)
        numberOfAcquiredChannels = self.device.GetNumberOfAcquiredChannels()

        # Allocate memory for the acquisition buffer.
        receiveBufferBufferLength = frameLength * duration * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(receiveBufferBufferLength)

        numberOfDataCalls = int(duration * UnicornPy.SamplingRate/ frameLength)

        # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
        for call in range(0, numberOfDataCalls):
            self.device.GetData(frameLength ,receiveBuffer,receiveBufferBufferLength)

        data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels)
        data = np.reshape(data, (frameLength, numberOfAcquiredChannels))
        self.device.StopAcquisition()
        return data

