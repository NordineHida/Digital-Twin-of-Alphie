"""
File:          Task_GoToCoordinates.py
Date:          February 2024
Description:   Algorithm to move a robot to specified coordinates
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *
from NetworkManager import *


def go_to_coordinates(robot: RobotUp, target_coordinate: Coordinates):
    """
    Move the robot to the specified target coordinates.

    Args:
        robot (RobotUp) : The selected robot
        target_coordinate (Coordinates): The target coordinates.
    """
    print(f"{robot.getName()} : Moving to coordinates: ({target_coordinate.x}, {target_coordinate.y})")

    # Get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    # Initialise PositionManager with the robot
    position_manager = PositionManager(robot)
    movement_manager = MovementManager(robot)
    network_manager = NetworkManager(robot)

    # Tolerance values
    arrival_tolerance = 0.1
    angle_tolerance = 3.0

    target_achieved = False
    priority_message = False

    # Main loop:
    while robot.step(timestep) != -1 and not target_achieved and not priority_message:

        robot.step(timestep)

        # Check if the robot has arrived at the target position
        if not position_manager.is_arrived(target_coordinate, arrival_tolerance):
            # Get the bearing angle to the target coordinates
            angle_to_destination = position_manager.get_bearing_to_coordinate(target_coordinate)

            # Rotate the robot until it faces the target coordinates
            position_manager.rotate_to_destination(angle_to_destination, angle_tolerance)

            # Move forward
            movement_manager.move_forward()

        else:
            # Stop the robot when the target position is reached
            movement_manager.stop()
            print("Target position reached!")
            target_achieved = True

        case_executed = network_manager.update()
        priority_message = case_executed == MESSAGE_TYPE_PRIORITY.STOP.value
