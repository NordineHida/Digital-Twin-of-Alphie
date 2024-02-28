"""
File:           InitialisationManager.py
Date:           February 2024
Description:    Initialise all devices of the robot (gps, compass, receiver ...)
Author:         Nordine HIDA
Modifications:
"""

from RobotUpInitializer import *


class InitialisationManager:
    """
    Initialize all devices of the robot (gps, compass, ...)
    Must be called right after the creation of the entity (robot, remote, ...)
    """

    @staticmethod
    def init_devices(robot: RobotUpInitializer):
        """
        Enable all devices of the robot with a simulation time_step of 10 (ms).
        time_step value can be modified.

        Args:
            robot (RobotUpInitializer): The robot to initialize
        """
        time_step = 10

        # Loop through each device and attempt to enable it if the enable method exists
        for device_name in robot.robot.devices:
            device = robot.robot.devices[device_name]
            if hasattr(device, 'enable') and callable(getattr(device, 'enable')):
                device.enable(time_step)
                print(robot.getName(), " ", device_name, " has been enabled")
