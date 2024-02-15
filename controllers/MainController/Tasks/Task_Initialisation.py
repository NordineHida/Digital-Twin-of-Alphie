"""
File:           Task_Initialisation.py
Date:           February 2024
Description:    Initialise all devices of the robot (gps, compass, receiver ...)
                |!| Must be called right after the creation of the robot (or remote, ...)
Author:         Nordine HIDA
Modifications:
"""

from MainController.Managers.InitialisationManager import *


class Task_Initialisation:
    """
    Initialise all devices of the robot (gps, compass, receiver ...)
    |!| Must be called right after the creation of the robot (or remote, ...)
    """

    @staticmethod
    def init_devices(robot: Robot):
        """
        Call the manager to initialize all devices of the robot.

        Args:
            robot (Robot): The robot (or remote) to be initialized.
        """
        InitialisationManager.init_devices(robot)
