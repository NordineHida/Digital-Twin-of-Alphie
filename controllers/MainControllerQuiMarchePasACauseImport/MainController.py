"""
File:           MainController.py
Date:           February 2024
Description:    Main program executed by each track robot.
                Here you can build your algorithm by using tasks.
Author:         Nordine HIDA
Modifications:
"""

import sys
import os

# Obtenez le chemin absolu du répertoire parent du répertoire contenant MainController.py
parent_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(parent_dir, ".."))
sys.path.append(project_dir)

from Tasks.Task_Initialisation import Task_Initialisation

from controller.robot import Robot


# Constant of webots
TIME_STEP = 32

# The unique allowed creation of robot
robot = Robot()

# Initialisation of it devices
Task_Initialisation.init_devices(robot)
"""
# task_goToCoordinates = Task_GoToCoordinates(robot)

keyboard = Keyboard(10)
keyboard.enable(10)

key = None

# Main loop in which you can place your tasks to build an algorithm
while key is None:
    key = keyboard.getKey()
    print(key, " pressed")
    # task_goToCoordinates.go_to_coordinates(Coordinates(2, 2))
"""
