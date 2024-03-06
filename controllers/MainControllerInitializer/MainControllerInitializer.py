"""
File:           MainControllerInitializer.py
Date:           February 2024
Description:    This controller gives a sense of group awareness to each of the robots (+ remote)
                by initializing the robots' known_robots dictionary.
                It calls the roll in order to get all robot's name (without the remote)
                and share the list to all of them (+ the remote).
Author:         Nordine HIDA
Modifications:
"""

from InitialisationManager import *
from NetworkManagerInitialiseur import *
from RobotUpInitializer import *

# INITIALIZATION ---------


# The unique allowed creation of robot
robot = RobotUpInitializer()

# Number of robot in the simulation (without the remote and the initializer)
NUMBER_ROBOT = robot.getNumberOfRobots()

time_step = robot.getBasicTimeStep()

# Initialisation of robot devices
init_devices(robot)

network_manager = NetworkManagerInitialiseur(robot)
# ---------------------------------

# Loop until all robots are detected
while len(robot.known_robots) < NUMBER_ROBOT:
    network_manager.update()
    robot.step(int(time_step))

print("---------------------------------- INITIALIZATION DONE ! ----------------------------------")
print(NUMBER_ROBOT, "robots found :")
for robot_name, current_task in robot.known_robots.items():
    print(f"Robot : {robot_name}, Current task : {current_task}")
print("-------------------------------------------------------------------------------------------")

# We send all the robot names in a concatenation separated by ':'
all_known_robots = ":".join(robot.known_robots.keys())
message = Message(robot.getName(), MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE, 0, all_known_robots)
network_manager.communication.send_message(message)
