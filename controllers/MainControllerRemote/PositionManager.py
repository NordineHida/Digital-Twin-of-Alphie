"""
File:          PositioningManager.py
Date:          February 2024
Description:   Manage the position and orientation of the remote to get it position and orientation
Author:        Nordine HIDA
Modifications:
"""

import math
from Coordinates import *
from RobotUp import *


class PositionManager:
    """
    Manages the position and orientation of the track robot.
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the PositionManager and the MovementManager with a robot instance.

        |!| the gps of the robot should be called "gps" (default name in webots) \n
        |!| the compass of the robot should be called "compass" (default name in webots)

        :param robot (RobotUp) : The robot instance.
        """
        self.robot = robot
        self.compass = robot.getDevice("compass")
        self.gps = robot.getDevice("gps")
        self.time_step = int(self.robot.getBasicTimeStep())

    def get_bearing_to_coordinate(self, target_position):
        """
        Get the bearing angle in degrees to reach a specific coordinate.
        :param target_position: The target coordinates.
        :return: The bearing angle in degrees.
        """
        robot_position = self.get_position()

        rad = math.atan2(target_position.y - robot_position.y, target_position.x - robot_position.x)
        # Convert angle to degrees
        bearing = math.degrees(rad)
        # Ensure the angle is in the range [0, 360]
        if bearing < 0.0:
            bearing += 360.0
        return bearing

    def get_heading_robot(self):
        """
        Get the heading angle of the robot based on compass readings.

        :return: The heading angle in degrees.
        """
        compass_values = self.compass.getValues()

        rad = math.atan2(compass_values[0], compass_values[1])
        heading_angle_degrees = math.degrees(rad)

        if heading_angle_degrees < 0.0:
            heading_angle_degrees += 360.0

        return heading_angle_degrees

    def get_position(self):
        """
        Get the position of the robot.

        :return: Coordinates of the robot.
        """
        position = self.gps.getValues()
        return Coordinates(position[0], position[1])

