"""
File:           NetworkManager.py
Date:           February 2024
Description:    Manage the network of communication between robots,
                facilitating the retrieval of nearby robots and
                determining which ones should take action.
Author:         Nordine HIDA
Modifications:
"""

from CommunicationManager import *


class NetworkManager:
    """
    Manage the network of communication between robots,
    facilitating the retrieval of nearby robots and
    determining which ones should take action.
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the NetworkManager.

        Args:
            robot (Robot): The robot (a remote can be considered as a robot)
        """
        self.robot = robot
        self.accessible_robots = []
        self.accessible_free_robots = []
        self.communication_manager = CommunicationManager(robot)
        self.time_step = int(self.robot.getBasicTimeStep())
