"""
File:           Task_Initialisation.py
Date:           February 2024
Description:    Initialise all devices of the robot (gps, compass, receiver ...)
                |!| Must be called right after the creation of the robot (or remote, ...)

                Then it start the loop of simulation -> wait a message and process it
Author:         Nordine HIDA
Modifications:
"""

from InitialisationManager import *
from Task_Communication import *
from Task_GoToCoordinates import *

class Task_Initialisation:
    """
    Initialise all devices of the robot (gps, compass, receiver ...)
    |!| Must be called right after the creation of the robot (or remote, ...)
    """

    def __init__(self, robot: Robot):
        """
        Initialize of the robot

        Args:
            robot (Robot): The robot (or remote) to be initialized.
        """
        self.robot = robot

        # communication manager
        self.communication = Task_Communication(robot).network_manager.communication_manager

    def init_devices(self):
        """
        Call the manager to initialize all devices of the robot.
        """
        InitialisationManager.init_devices(self.robot)

    def update(self):
        """
        Receive
        """
        message = self.communication.receive_message()

        # If the message isn't empty/none
        if message:
            id_sender, message_type, payload = message.split(";")
            print("Message reçu : ", message.message_type)

            match message.message_type:
                case MESSAGE_TYPE_PRIORITY.REPORT_STATUS:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.REPORT_POSITION:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.POSITION:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.OK:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.PRESENT:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.PRESENT_FREE:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.STOP:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES:
                    task_GTC = Task_GoToCoordinates(self.robot)
                    x, y = payload.split("-")
                    task_GTC.go_to_coordinates(Coordinates(x, y))
                case MESSAGE_TYPE_PRIORITY.WHO_IS_PRESENT:
                    # to do
                    pass
                case MESSAGE_TYPE_PRIORITY.WHO_IS_PRESENT_AND_FREE:
                    # to do
                    pass
                case _:
                    pass


