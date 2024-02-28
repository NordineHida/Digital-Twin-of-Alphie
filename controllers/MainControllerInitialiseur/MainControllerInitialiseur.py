"""
File:           MainControllerInitialiseur.py
Date:           February 2024
Description:    Main program executed by the remote to send tasks to nearby robots.
                Here you can build your algorithm by sending message task.
Author:         Nordine HIDA
Modifications:
"""

from Task_Initialisation import *
from NetworkManagerInitialiseur import *
from RobotUpInitializer import *

# INITIALIZATION ---------

# Number of robot in the simulation (without the remote)
NUMBER_ROBOT = 3

# The unique allowed creation of robot
robot = RobotUpInitializer()
time_step = robot.getBasicTimeStep()

# Initialisation of robot devices
task_Initialisation = Task_Initialisation(robot)

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

# Ici send la liste known_robot a tout les robots et que chaque robot les initialise a un nouvelle etat (MESSAGE_TYPE_PRIORITY)
# du style "STATUS_DOWN, ou OUT OF RANGE ou INACTIVE



