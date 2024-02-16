"""
File:           MainController.py
Date:           February 2024
Description:    Main program executed by each track robot.
                Here you can build your algorithm by using tasks.
Author:         Nordine HIDA
Modifications:
"""

from Task_Initialisation import *
from Task_GoToCoordinates import *

# region INITIALISATION

# The unique allowed creation of robot
robot = Robot()
# Initialisation of robot devices
Task_Initialisation.init_devices(robot)

# Initialisation of tasks
task_GoToCoordinates = Task_GoToCoordinates(robot)

# endregion

# Place here your tasks to build an algorithm
task_GoToCoordinates.go_to_coordinates(Coordinates(1, 1))
task_GoToCoordinates.go_to_coordinates(Coordinates(-1, -1))
