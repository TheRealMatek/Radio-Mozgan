import UnicornPy
import numpy as np

'''
This class is a wrapper for the UnicornPy library. It provides a static method to get a sample of duration from the Unicorn device.
'''
class Unicorn:
    @staticmethod
    def getSample(duration):
        deviceList = UnicornPy.GetAvailableDevices(True)
        if len(deviceList) <= 0 or deviceList is None:
            raise Exception("No device available.Please pair with a Unicorn first.")
        device = UnicornPy.Unicorn(deviceList[0])

        frameLength = 1
        device.StartAcquisition(True)
        numberOfAcquiredChannels = device.GetNumberOfAcquiredChannels()

        # Allocate memory for the acquisition buffer.
        receiveBufferBufferLength = frameLength * duration * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(receiveBufferBufferLength)

        numberOfDataCalls = int(duration * UnicornPy.SamplingRate/ frameLength)

        # Receives the configured number of samples from the Unicorn device and writes it to the acquisition buffer.
        for call in range(0, numberOfDataCalls):
            device.GetData(frameLength ,receiveBuffer,receiveBufferBufferLength)

        data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels)
        data = np.reshape(data, (frameLength, numberOfAcquiredChannels))
        device.StopAcquisition()
        return data

