"""
File:           NetworkManager.py
Date:           February 2024
Description:    Manage the network of communication between robots,
                facilitating the retrieval of nearby robots and
                determining which ones should take action.
Author:         Nordine HIDA
Modifications:
"""

from CommunicationManager import *
import time
import random


class NetworkManager:
    """
    Manage the network of communication between robots,
    facilitating the retrieval of nearby robots and
    determining which ones should take action.
    """

    def __init__(self, robot: Robot):
        """
        Initialize the NetworkManager.

        Args:
            robot (Robot): The robot (a remote can be considered as a robot)
        """
        self.robot = robot
        self.accessible_robots = []
        self.accessible_free_robots = []
        self.communication_manager = CommunicationManager(robot)
        self.time_step = int(self.robot.getBasicTimeStep())

    def get_who_is_there(self) -> list:
        """
        Retrieve the IDs of the nearby robots.

        Returns:
            list: A list of strings representing the IDs of the nearby robots.
        """
        # Send a message to inquire who is nearby
        message = Message(self.robot.getName(), MESSAGE_TYPE_PRIORITY.WHO_IS_PRESENT, "")
        self.communication_manager.send_message(message)

        responses = []
        for _ in range(50):
            received_message = self.communication_manager.receive_message()

            # If the message isn't empty
            if received_message:
                #  If the message is of type "PRESENT" we add the sender to our list
                if received_message.message_type == MESSAGE_TYPE_PRIORITY.PRESENT:
                    responses.append(received_message.id_sender)

        # Update the list of accessible robots
        self.accessible_robots = responses

        # Sort the list of accessible robots in ascending order
        self.accessible_robots.sort()

        return self.accessible_robots

    def get_who_is_there_free(self):
        """
        Retrieve the IDs of the nearby robots that are free

        Returns:
            list: A list of strings representing the IDs of the nearby free robots
        """
        # Send a message to inquire who is nearby
        message = Message(self.robot.getName(), MESSAGE_TYPE_PRIORITY.WHO_IS_PRESENT_AND_FREE, "")
        self.communication_manager.send_message(message)

        # Listen for responses for up to 3 seconds
        start_time = time.time()
        responses = []
        while time.time() - start_time < 3:
            received_message = self.communication_manager.receive_message()
            # If the message is of type "PRESENT" we add the sender to our list
            if received_message.message_type == MESSAGE_TYPE_PRIORITY.PRESENT_FREE:
                responses.append(received_message.id_sender)

        # Update the list of accessible robots
        self.accessible_free_robots = responses

        # Sort the list of accessible robots in ascending order
        self.accessible_free_robots.sort()

        return self.accessible_free_robots

    def get_who_is_next(self) -> str:
        """
        Retrieve the ID of the next accessible free robot.

        Returns:
            str: The ID of the next accessible robot.
        """
        return self.accessible_free_robots[0]
