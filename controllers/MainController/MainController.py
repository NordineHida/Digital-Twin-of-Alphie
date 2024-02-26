"""
File:           MainController.py
Date:           February 2024
Description:    Main program executed by each track robot.
                It init the robot and start the main loop of simulation
Author:         Nordine HIDA
Modifications:
"""

from Task_Initialisation import *
from NetworkManager import *
from RobotUp import *

# INITIALIZATION ---------

# The unique allowed creation of robot
robot = RobotUp()
time_step = robot.getBasicTimeStep()
# Initialisation of robot devices
task_Initialisation = Task_Initialisation(robot)

network_manager = NetworkManager(robot)
# ------------------------

# Main loop of simulation
while True:
    network_manager.update()
    robot.step(int(time_step))
