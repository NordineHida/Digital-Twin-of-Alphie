"""GoToCoordinatePython controller."""
# You may need to import some classes of the controller module. Ex:
# from controller import Robot, Motor, DistanceSensor
from controller import Robot

# Import PositionManager et MovementManager
from PositionManager import *
from MovementManager import MovementManager

# Create the Robot instance.
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Initialiser PositionManager et MovementManager
position_manager = PositionManager(robot)
movement_manager = MovementManager(robot)

# Define target position (X,Y)
target_position = Coordinates(2, 2)

# Tolerance values
arrival_tolerance = 0.01
angle_tolerance = 3.0

# Main loop:
# - Perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    # val = ds.getValue()

    # Get current position
    current_position = position_manager.get_position()

    # Process sensor data here.

    # Check if the robot has arrived at the target position
    if not position_manager.is_arrived(current_position, target_position, arrival_tolerance):
        # Get the bearing angle to the target coordinates
        angle_to_destination = position_manager.get_bearing_to_coordinate(current_position, target_position)

        # Rotate the robot until it faces the target coordinates
        position_manager.rotate_to_destination(angle_to_destination, angle_tolerance)

        # Move forward
        movement_manager.move_forward()
    else:
        # Stop the robot when the target position is reached
        movement_manager.stop()
        print("Target position reached!")
        # Enter here exit cleanup code.
        break
