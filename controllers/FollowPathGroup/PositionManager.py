"""
File:          PositioningManager.py
Date:          February 2024
Description:   Manage the position and orientation of the track robot. It allows you to rotate to coordinates.
Author:        Nordine HIDA
Modifications:
"""

import math
from MovementManager import *
from Coordinates import *


class PositionManager:
    """
    Manages the position and orientation of the track robot.
    """

    def __init__(self, robot):
        """
        Initialize the PositionManager and the MovementManager with a robot instance.
        :param robot: The robot instance.
        """
        self.robot = robot
        self.time_step = int(self.robot.getBasicTimeStep())
        self.movement_manager = MovementManager(self.robot)

    def get_movement_manager(self):
        """
        Get the MovementManager of the instance (To avoid the multiple creation of movementManager)
        :return: the MovementManager of the PositionManager
        """
        return self.movement_manager

    def get_bearing_to_coordinate(self, robot_position, target_position):
        """
        Get the bearing angle in degrees to reach a specific coordinate.
        :param robot_position: The current position coordinates of the robot.
        :param target_position: The target coordinates.
        :return: The bearing angle in degrees.
        """
        rad = math.atan2(target_position.y - robot_position.y, target_position.x - robot_position.x)
        # Convert angle to degrees
        bearing = math.degrees(rad)
        # Ensure the angle is in the range [0, 360]
        if bearing < 0.0:
            bearing += 360.0
        return bearing

    def get_heading_robot(self, compass):
        """
        Get the heading angle of the robot based on compass readings.
        :param compass: The compass device of the robot.
        :return: The heading angle in degrees.
        """
        compass_values = compass.getValues()
        rad = math.atan2(compass_values[0], compass_values[1])
        heading_angle_degrees = math.degrees(rad)
        if heading_angle_degrees < 0.0:
            heading_angle_degrees += 360.0
        return heading_angle_degrees

    def rotate_to_destination(self, compass, angle_to_destination, tolerance):
        """
        Rotate the robot until it reaches the specified angle.
        :param compass: The compass device of the robot.
        :param angle_to_destination: The angle to the destination coordinates in degrees.
        :param tolerance: The tolerance to consider the destination reached.
        """
        heading_robot_angle = self.get_heading_robot(compass)
        angle_difference = angle_to_destination - heading_robot_angle
        if angle_difference < -180.0:
            angle_difference += 360.0
        elif angle_difference >= 180.0:
            angle_difference -= 360.0
        if not abs(angle_difference) < tolerance:
            if angle_difference < 0:
                self.movement_manager.move_right()
            else:
                self.movement_manager.move_left()
            self.robot.step(self.time_step)
            self.rotate_to_destination(compass, angle_to_destination, tolerance)
        else:
            self.movement_manager.move_forward()
            self.robot.step(self.time_step)

    def get_position(self, gps):
        """
        Get the position of the robot.
        :param gps: The GPS device of the robot.
        :return: Coordinates of the robot.
        """
        position = self.robot.getDevice("gps").getValues()
        return Coordinates(position[0], position[1])

    def is_arrived(self, current, target, tolerance):
        """
        Check if the robot has arrived at the target coordinates with a tolerance.
        :param current: The current coordinates of the robot.
        :param target: The target coordinates.
        :param tolerance: The tolerance value for both X and Y coordinates.
        :return: True if the robot has arrived, False otherwise.
        """
        difference_x = abs(current.x - target.x)
        difference_y = abs(current.y - target.y)
        return difference_x < tolerance and difference_y < tolerance
