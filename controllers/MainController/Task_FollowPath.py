"""
File:           Task_FollowPath.py
Date:           February 2024
Description:    This task's goal is to make the robot follow a path composed of several target coordinates.
Author:         Nordine HIDA
Modifications:
"""

from Task_GoToCoordinates import *


class Task_FollowPath:
    """
    This task is responsible for making the robot follow a path composed of several target coordinates.
    """

    def __init__(self, robot: RobotUp, coordinates_path: list[Coordinates]):
        """
        Initialize the Task_FollowPath instance.

        Args:
            robot (RobotUp): The robot instance.
            coordinates_path (list[Coordinates]): The list of target coordinates.
        """
        self.robot = robot
        self.coordinates_path = coordinates_path
        self.task_GoToCoordinates = Task_GoToCoordinates(robot)

    def follow_path(self):
        """
        Make the robot follow the path composed of several target coordinates.
        """
        for target_position in self.coordinates_path:
            self.task_GoToCoordinates.go_to_coordinates(target_position)
