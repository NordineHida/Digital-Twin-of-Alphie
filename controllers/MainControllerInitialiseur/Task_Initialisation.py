"""
File:           Task_Initialisation.py
Date:           February 2024
Description:    Initialise all devices of the robot (gps, compass, receiver ...)
                |!| Must be called right after the creation of the robot (or remote, ...)

                Then it start the loop of simulation -> wait a message and process it
Author:         Nordine HIDA
Modifications:
"""

from InitialisationManager import *
from CommunicationManager import *


class Task_Initialisation:
    """
    Initialise all devices of the robot (gps, compass, receiver ...)
    |!| Must be called right after the creation of the robot (or remote, ...)
    """

    def __init__(self, robot: RobotUpInitializer):
        """
        Initialize all devices of the robot (or remote)

        Args:
            robot (RobotUpInitializer): The robot instance to be initialized.
        """
        self.robot = robot
        self.robot_name = self.robot.getName()

        # Initialize devices
        InitialisationManager.init_devices(self.robot)





