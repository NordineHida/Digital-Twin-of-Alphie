"""
File:          GoToCoordinateManager.py
Date:          February 2024
Description:   Algorithm to move a robot to specified coordinates
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *

# Distance from which we consider the robot has arrived
ARRIVAL_TOLERANCE = 0.01

# Angle difference from which we consider the robot is well oriented
ANGLE_TOLERANCE = 3.0




class GoToCoordinate:
    @staticmethod
    def go_to_coordinate(target_coordinate, robot):
        # Create the Robot instance.
        robot = robot

        print(f"{robot.getName()} : Moving to coordinates: ({target_coordinate.x}, {target_coordinate.y})")

        # Get and enable measuring devices
        compass = robot.getDevice("compass")
        compass.enable(10)
        gps = robot.getDevice("gps")
        gps.enable(10)

        # Get the time step of the current world.
        timestep = int(robot.getBasicTimeStep())

        # Initialise PositionManager et MovementManager with the robot
        position_manager = PositionManager(robot)
        movement_manager = position_manager.get_movement_manager()

        target_achieved = False
        # Main loop:
        while robot.step(timestep) != -1 and not target_achieved:

            # Get current position
            current_position = position_manager.get_position(gps)

            # Check if the robot has arrived at the target position
            if not position_manager.is_arrived(current_position, target_coordinate, ARRIVAL_TOLERANCE):
                # Get the bearing angle to the target coordinates
                angle_to_destination = position_manager.get_bearing_to_coordinate(current_position, target_coordinate)

                # Rotate the robot until it faces the target coordinates
                position_manager.rotate_to_destination(compass, angle_to_destination, ANGLE_TOLERANCE)

                # Move forward
                movement_manager.move_forward()
            else:
                # Stop the robot when the target position is reached
                movement_manager.stop()
                print("Target position reached!")
                target_achieved = True
