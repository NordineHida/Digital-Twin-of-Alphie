"""
File:           InitialisationManager.py
Date:           February 2024
Description:    Initialise all devices of the remote (gps, compass, receiver ...)
Author:         Nordine HIDA
Modifications:
"""

from RobotUpRemote import *


def init_devices(remote: RobotUpRemote):
    """
    Enable all devices of the remote with a simulation time_step of 10 (ms).
    time_step value can be modified.

    Args:
        remote (RobotUpRemote): The remote to initialize
    """
    time_step = 10

    # Loop through each device and attempt to enable it if the enable method exists
    for device_name in remote.remote.devices:
        device = remote.remote.devices[device_name]
        if hasattr(device, 'enable') and callable(getattr(device, 'enable')):
            device.enable(time_step)

    print(remote.getName(), " has been enabled")
