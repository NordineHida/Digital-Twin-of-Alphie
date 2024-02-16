"""
File:          Task_GoToCoordinates.py
Date:          February 2024
Description:   Algorithm to move a robot to specified coordinates
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *
from CommunicationManager import *
from controller import Robot


class Task_GoToCoordinates:
    """
    Algorithm to move a robot to specified coordinates.
    """

    def __init__(self, robot: Robot):
        """
        Initialize the GoToCoordinate algorithm.

        Args:
            robot (Robot): The robot instance.
        """
        self.robot = robot
        self.movement_manager = MovementManager(robot)

    def go_to_coordinates(self, target_coordinate: Coordinates):
        """
        Move the robot to the specified target coordinates.

        Args:
            target_coordinate (Coordinates): The target coordinates.
        """
        print(f"{self.robot.getName()} : Moving to coordinates: ({target_coordinate.x}, {target_coordinate.y})")

        # Get the time step of the current world.
        timestep = int(self.robot.getBasicTimeStep())

        # Initialise PositionManager with the robot
        position_manager = PositionManager(self.robot)

        # Initialise CommunicationManager to check if a message has been sent
        communication_manager = CommunicationManager(self.robot)

        # Tolerance values
        arrival_tolerance = 0.01
        angle_tolerance = 3.0

        target_achieved = False

        # Main loop:
        while self.robot.step(timestep) != -1 and not target_achieved:

            # Check if a message has been sent and handle it before continuing the task.
            if communication_manager.receiver.getQueueLength() > 0:
                communication_manager.check_messages(MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES)

            # Check if the robot has arrived at the target position
            if not position_manager.is_arrived(target_coordinate, arrival_tolerance):
                # Get the bearing angle to the target coordinates
                angle_to_destination = position_manager.get_bearing_to_coordinate(target_coordinate)

                # Rotate the robot until it faces the target coordinates
                position_manager.rotate_to_destination(angle_to_destination, angle_tolerance)

                # Move forward
                self.movement_manager.move_forward()
            else:
                # Stop the robot when the target position is reached
                self.movement_manager.stop()
                print("Target position reached!")
                target_achieved = True
