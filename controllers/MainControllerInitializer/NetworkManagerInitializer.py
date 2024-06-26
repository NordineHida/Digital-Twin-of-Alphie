"""
File:           NetworkManagerInitializer.py
Date:           February 2024
Description:    Call the roll in order to get all robot's name in the simulation.
Author:         Nordine HIDA
Modifications:
"""

from CommunicationManager import *


class NetworkManagerInitialiseur:
    """
    Manage the network of communication between the remote and robots.
    It sends messages bound to keys and reacts to incoming messages.
    """

    def __init__(self, robot: RobotUpInitializer):
        """
        Initialize the NetworkManager.

        Args:
            robot (RobotUpInitializer): The robot (a remote can be considered as a robot)
        """
        self.robot = robot
        self.robot_name = self.robot.getName()

        self.communication = CommunicationManager(self.robot)

        self.started = False

    def update(self):
        """
        Call the roll and try to get all robots.
        """

        if not self.started:
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL, 0, ""))
            self.robot.is_callrolling = True
            self.started = True

        # try to receive a message and add it to the robot's list
        self.communication.receive_message()

        # Check if the list of messages is not empty
        if self.robot.list_messages:
            # Getting the first message and remove it from the list
            message = self.robot.list_messages[0]
            self.robot.list_messages.pop(0)

            id_sender = message.id_sender
            message_type = MESSAGE_TYPE_PRIORITY.from_string(message.message_type)
            payload = message.payload

            match message_type:

                case MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL:
                    self.case_REPORT_BEGIN_ROLLCALL(id_sender, payload)

                case _:
                    print("Unknown message received")

    def case_REPORT_BEGIN_ROLLCALL(self, id_sender, payload):
        """
        It listens the answer of other robots and add them to it list of known robot
        """
        self.robot.known_robots[id_sender] = payload
