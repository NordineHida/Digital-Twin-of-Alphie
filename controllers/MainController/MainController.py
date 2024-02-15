"""
File:           MainController.py
Date:           February 2024
Description:    Main program executed by each track robot.
                Here you can build your algorithm by using tasks.
Author:         Nordine HIDA
Modifications:
"""

from controller import Keyboard
from MainController.Tasks.Task_Initialisation import *
from MainController.Tasks.Task_Communication import *
from MainController.Tasks.Task_FollowPath import *
from MainController.Tasks.Task_GoToCoordinates import *

# Constant of webots
TIME_STEP = 32

# The unique allowed creation of robot
robot = Robot()

# Initialisation of it devices
Task_Initialisation.init_devices(robot)

keyboard = Keyboard(10)
keyboard.enable(10)

key = None

# Main loop in which you can place your tasks to build an algorithm
while key is None:
    key = keyboard.getKey()
    print(key, " pressed")
    Task_GoToCoordinate(robot).go_to_coordinates(Coordinates(2, 2))


