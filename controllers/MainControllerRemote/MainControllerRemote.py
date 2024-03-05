"""
File:           MainControllerInitialiseur.py
Date:           February 2024
Description:    Main program executed by the remote to send tasks to nearby robots.
                Here you can build your algorithm by sending message task.
Author:         Nordine HIDA
Modifications:
"""

from InitialisationManager import *
from NetworkManagerRemote import *
from RobotUpRemote import *

# INITIALIZATION ---------

# The unique allowed creation of robot
robot = RobotUpRemote()
time_step = robot.getBasicTimeStep()

# Initialisation of robot devices
init_devices(robot)

network_manager = NetworkManagerRemote(robot)
# ---------------------------------

# Main loop of simulation
while True:
    network_manager.update()
    robot.step(int(time_step))








