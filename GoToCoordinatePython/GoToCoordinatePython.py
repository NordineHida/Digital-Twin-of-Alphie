"""
File:          GoToCoordinate.py
Date:          February 2024
Description:   The robot will turn on itself until it is facing the indicated coordinates, then it will move forward until it reaches the goal.
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *
from MovementManager import MovementManager
from controller import Robot

# region Initialisation

# Create the Robot instance.
robot = Robot()

# Get and enable measuring devices
compass = robot.getDevice("compass")
compass.enable(10)
gps = robot.getDevice("gps")
gps.enable(10)

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Initialise PositionManager et MovementManager with the robot
position_manager = PositionManager(robot)
movement_manager = MovementManager(robot)

# Define target position (X,Y)
target_position = Coordinates(2, 2)

# Tolerance values
arrival_tolerance = 0.01
angle_tolerance = 3.0

target_achieved = False
# endregion

# Main loop:
# - Perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1 and not target_achieved:
    # Get current position
    current_position = position_manager.get_position(gps)

    # Check if the robot has arrived at the target position
    if not position_manager.is_arrived(current_position, target_position, arrival_tolerance):
        # Get the bearing angle to the target coordinates
        angle_to_destination = position_manager.get_bearing_to_coordinate(current_position, target_position)

        # Rotate the robot until it faces the target coordinates
        position_manager.rotate_to_destination(compass, angle_to_destination, angle_tolerance)

        # Move forward
        movement_manager.move_forward()
    else:
        # Stop the robot when the target position is reached
        movement_manager.stop()
        print("Target position reached!")
        target_achieved = True
