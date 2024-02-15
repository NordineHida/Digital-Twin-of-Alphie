"""
File:           InitialisationManager.py
Date:           February 2024
Description:    Initialise all devices of the robot (gps, compass, receiver ...)
                |!| Must be called right after the creation of the entity (robot, remote, ...)
Author:         Nordine HIDA
Modifications:
"""

from controller.robot import *

class InitialisationManager:
    """
    Initialize all devices of the robot (gps, compass, ...)
    Must be called right after the creation of the entity (robot, remote, ...)
    """

    @staticmethod
    def init_devices(robot: Robot):
        """
        Enable all devices of the robot with a simulation time_step of 10 (ms).
        time_step value can be modified.

        Args:
            robot (Robot): The robot to initialize
        """
        time_step = 10

        # Loop through each device and attempt to enable it if the enable method exists
        for device_name in robot.devices:
            device = robot.devices[device_name]
            if hasattr(device, 'enable') and callable(getattr(device, 'enable')):
                device.enable(time_step)