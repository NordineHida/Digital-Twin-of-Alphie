"""
File:           MainController.py
Date:           February 2024
Description:    Main program executed by each track robot.
                It init the robot and start the main loop of simulation
Author:         Nordine HIDA
Modifications:
"""

from Task_Initialisation import *

# INITIALIZATION ---------

# The unique allowed creation of robot
robot = Robot()
# Initialisation of robot devices
task_Initialisation = Task_Initialisation(robot)
task_Initialisation.init_devices()
# ------------------------

# Main loop of simulation
while True:
    task_Initialisation.update()
