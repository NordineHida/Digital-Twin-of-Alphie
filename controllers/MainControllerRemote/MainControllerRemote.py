"""
File:           MainControllerRemote.py
Date:           February 2024
Description:    Main program executed by the remote to send tasks to nearby robots.
                Here you can build your algorithm by sending message task.
Author:         Nordine HIDA
Modifications:
"""

from Task_Initialisation import *


# INITIALIZATION ---------

# The unique allowed creation of robot
robot = Robot()
robot_name = robot.getName()
# Initialisation of robot devices
task_Initialisation = Task_Initialisation(robot)
task_Initialisation.init_devices()
# ------------------------

task_Comm = Task_Communication(robot)
communication = task_Comm.network_manager.communication_manager

# Here you can send messages
communication.send_message(Message(robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, "2-2"))
