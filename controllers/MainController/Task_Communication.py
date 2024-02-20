"""
File:           Task_Communication.py
Date:           February 2024
Description:    This task is responsible for determining nearby robots and establishing the order of execution of tasks
                in the robot's network.
Author:         Nordine HIDA
Modifications:
"""

from NetworkManager import *


class Task_Communication:
    """
    This task is responsible for determining nearby robots and establishing the order of execution of tasks
    in the robot's network.
    """

    def __init__(self, robot):
        """
        Initialize the TaskCommunication.

        Args:
            robot (Robot): The robot instance.
        """
        self.robot = robot
        self.network_manager = NetworkManager(robot)

