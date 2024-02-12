"""
File:          FollowPathGroup.py
Date:          February 2024
Description:   The robot will follow a path composed of several target coordinates.
Author:        Nordine HIDA
Modifications:
"""

from PositionManager import *
from MovementManager import MovementManager
from GoToCoordinateManager import GoToCoordinate
from controller import Robot


# region Initialisation

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
robot_name = robot.getName()

# Get and enable measuring devices
compass = robot.getDevice("compass")
compass.enable(10)
gps = robot.getDevice("gps")
gps.enable(10)
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
receiver.enable(10)


# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Initialise PositionManager et MovementManager with the robot
position_manager = PositionManager(robot)
movement_manager = MovementManager(robot)

# Tolerance values
arrival_tolerance = 0.01
angle_tolerance = 3.0

canMove = False
if robot_name == "Alphie":
    canMove = True
# endregion

print(robot_name, " go !")

# Main loop:
if canMove:
    # We simply go to each coordinate one by one
    for target_position in coordinates_path:
        print(f"{robot_name} : Moving to coordinates: ({target_position.x}, {target_position.y})")

        # Call the go_to_coordinate method from GoToCoordinate class
        GoToCoordinate.go_to_coordinate(target_position.x, target_position.y, robot)

        # Send a message to other robots with the coordinates
        message = f"arrive {target_position.x} {target_position.y}"
        emitter.send(message.encode())
else:
    # Main loop for other robots
    while robot.step(timestep) != -1:
        # Check for incoming messages
        while receiver.getQueueLength() > 0:
            # Get the received message
            message = receiver.getString()
            # Extract the destination coordinates from the message
            destination_x, destination_y = map(float, message.split()[1:])

            # Move towards the received destination coordinates
            GoToCoordinate.go_to_coordinate(destination_x, destination_y, robot)

            # Once the destination is reached, acknowledge the arrival by sending a message back to the sender
            acknowledgment_message = f"arrive {destination_x} {destination_y}"
            emitter.send(acknowledgment_message.encode())

            # Discard the processed message
            receiver.nextPacket()



