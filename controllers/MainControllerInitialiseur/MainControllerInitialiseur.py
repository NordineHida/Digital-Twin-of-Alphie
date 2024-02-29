"""
File:           MainControllerInitialiseur.py
Date:           February 2024
Description:    This method initializes the robots' known_robots dictionary.
                It retrieves the roster and then distributes all robot names to populate their lists.

                |!| YOU MUST MODIFY THE NUMBER_ROBOT CONSTANT TO INCLUDE ALL ROBOTS IN YOUR SIMULATION
Author:         Nordine HIDA
Modifications:
"""

from InitialisationManager import *
from NetworkManagerInitialiseur import *
from RobotUpInitializer import *

# INITIALIZATION ---------

# Number of robot in the simulation (without the remote)
# |!| MUST BE MODIFIED ACCORDING TO THE NUMBER OF ROBOTS IN THE SIMULATION |!|
NUMBER_ROBOT = 3

# The unique allowed creation of robot
robot = RobotUpInitializer()
time_step = robot.getBasicTimeStep()

# Initialisation of robot devices
init_devices(robot)

network_manager = NetworkManagerInitialiseur(robot)
# ---------------------------------

# Loop until all robots are detected
while len(robot.known_robots) < NUMBER_ROBOT:
    network_manager.update()
    robot.step(int(time_step))

print("----------------- INITIALIZATION DONE ! -----------------")
print(NUMBER_ROBOT, "robots found :")
for robot_name, current_task in robot.known_robots.items():
    print(f"Robot : {robot_name}, Current task : {current_task}")
print("---------------------------------------------------------")

# We send all the robot names in a concatenation separated by ':'
all_known_robots = ":".join(robot.known_robots.keys())
message = Message(robot.getName(), MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE, all_known_robots)
network_manager.communication.send_message(message)




