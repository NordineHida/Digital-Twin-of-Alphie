"""
File:          PositioningManager.py
Date:          February 2024
Description:   Manage the position and orientation of the track robot. It allows you to rotate to coordinates.
Author:        Nordine HIDA
Modifications:
"""

import math
from MovementManager import *

# Structure of coordinates
class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PositionManager:

    def __init__(self, robot):
        self.robot = robot
        self.time_step = int(self.robot.getBasicTimeStep())
        self.movement_manager = MovementManager(self.robot)

    # Get the bearing angle in degrees to reach a specific coordinate
    def get_bearing_to_coordinate(self, robot_position, target_position):
        # Calculate angle to the target coordinates in radians
        rad = math.atan2(target_position.y - robot_position.y, target_position.x - robot_position.x)
        print("target pos : X: ", target_position.x, " Y: ", target_position.y)
        print("robot pos : X: ", robot_position.x, " Y: ", robot_position.y)
        # Convert angle to degrees
        bearing = math.degrees(rad)
        # Ensure the angle is in the range [0, 360]
        if bearing < 0.0:
            bearing += 360.0

        print("angle to coordinate : ", bearing)
        return bearing

    # Get the heading angle of the robot based on compass readings
    def get_heading_robot(self, compass):
        # Get current compass values
        compass_values = compass.getValues()

        # Calculate heading angle in radians
        rad = math.atan2(compass_values[0], compass_values[1])

        # Convert angle to degrees
        heading_angle_degrees = math.degrees(rad)

        # Adjust angle to be in the range [0, 360)
        if heading_angle_degrees < 0.0:
            heading_angle_degrees += 360.0

        return heading_angle_degrees

    # Rotate the robot until it reaches the specified angle
    def rotate_to_destination(self, compass, angle_to_destination, tolerance):
        # Get the heading angle (where is looking) the robot
        heading_robot_angle = self.get_heading_robot(compass)

        # Calculate the angle difference between the robot's heading and the destination angle
        angle_difference = angle_to_destination - heading_robot_angle

        # Adjust angle difference to be in the range [-180, 180)
        if angle_difference < -180.0:
            angle_difference += 360.0
        elif angle_difference >= 180.0:
            angle_difference -= 360.0

        # Check tolerance to consider the destination reached
        if not abs(angle_difference) < tolerance:
            # Choose rotation direction based on the angle difference
            if angle_difference < 0:
                # Rotate right
                self.movement_manager.move_right()
            else:
                # Rotate left
                self.movement_manager.move_left()

            # Update the simulation
            self.robot.step(self.time_step)
            self.rotate_to_destination(compass, angle_to_destination, tolerance)  # Recursive call to continue rotation
        else:
            print("Angle reached!")
            # Move to the destination
            self.movement_manager.move_forward()
            self.robot.step(self.time_step)

    # Get the position of the robot
    def get_position(self, gps):
        position = gps.getValues()
        return Coordinates(position[0], position[1])

    # Check if the robot has arrived at the target coordinates with a tolerance
    def is_arrived(self, current, target, tolerance):
        difference_x = abs(current.x - target.x)
        difference_y = abs(current.y - target.y)
        return difference_x < tolerance and difference_y < tolerance

    # Calculate the vector to go from the current position to the target position
    def calculate_go_to(self, actual, target):
        return Coordinates(target.x - actual.x, target.y - actual.y)
