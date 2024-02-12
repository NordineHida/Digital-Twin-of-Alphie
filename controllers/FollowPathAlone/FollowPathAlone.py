"""
File:          FollowPathGroup.py
Date:          February 2024
Description:   The robot will follow a path composed of several target coordinates.
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *
from MovementManager import MovementManager
from controller import Robot

# Define the target coordinates path
coordinates_path = [
    Coordinates(2, 2),
    Coordinates(1, 1),
    Coordinates(0, 0),
    Coordinates(1, 0),
    Coordinates(-2, 3),
    Coordinates(-1, 3)
]

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

# Tolerance values
arrival_tolerance = 0.01
angle_tolerance = 3.0

# Main loop:
# We simply go to each coordinate one by one
for target_position in coordinates_path:
    target_achieved = False
    print(f"Moving to coordinates: ({target_position.x}, {target_position.y})")
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
            print(f"Reached coordinates: ({target_position.x}, {target_position.y})")
            target_achieved = True
