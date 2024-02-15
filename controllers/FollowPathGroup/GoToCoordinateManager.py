"""
File:          GoToCoordinateManager.py
Date:          February 2024
Description:   Algorithm to move a robot to specified coordinates
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *

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

        # Tolerance values
        arrival_tolerance = 0.01
        angle_tolerance = 3.0

        target_achieved = False
        # Main loop:
        while robot.step(timestep) != -1 and not target_achieved:

            # Get current position
            current_position = position_manager.get_position(gps)

            # Check if the robot has arrived at the target position
            if not position_manager.is_arrived(current_position, target_coordinate, arrival_tolerance):
                # Get the bearing angle to the target coordinates
                angle_to_destination = position_manager.get_bearing_to_coordinate(current_position, target_coordinate)

                # Rotate the robot until it faces the target coordinates
                position_manager.rotate_to_destination(compass, angle_to_destination, angle_tolerance)

                # Move forward
                movement_manager.move_forward()
            else:
                # Stop the robot when the target position is reached
                movement_manager.stop()
                print("Target position reached!")
                target_achieved = True
