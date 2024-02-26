"""
File:           Task_Initialisation.py
Date:           February 2024
Description:    Initialise all devices of the robot (gps, compass, receiver ...)
                |!| Must be called right after the creation of the robot (or remote, ...)

Author:         Nordine HIDA
Modifications:
"""

from InitialisationManager import *


class Task_Initialisation:
    """
    Initialise all devices of the robot (gps, compass, receiver ...)
    |!| Must be called right after the creation of the robot (or remote, ...)
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the robot.

        Args:
            robot (RobotUp): The robot (or remote) to be initialized.
        """
        self.robot = robot
        self.robot_name = self.robot.getName()

        # Initialize devices
        InitialisationManager.init_devices(self.robot)

