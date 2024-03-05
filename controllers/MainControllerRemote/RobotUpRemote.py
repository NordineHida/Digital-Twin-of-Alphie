"""
File:           RobotUpRemote.py
Date:           February 2024
Description:    Override of webots's remote with extra attributes, like a list of messages to process
Author:         Nordine HIDA
Modifications:
"""

from controller.robot import *
from Message import *
from typing import List


class RobotUpRemote:
    """
    RobotUpRemote class overrides the webots remote class with additional attributes and methods.
    """

    def __init__(self):
        """
        Constructor for RobotUpRemote class. Init all attributes
        """
        self.remote = Robot()
        self.list_messages: List[Message] = []

        # list of nearby robots
        self.known_robots = {}

        # First free remote in known_robots. Messages will be sent to it
        self.first_rob = ""

        # boolean to remember if the remote has already call rolled
        self.is_callrolling = False

    def getDevice(self, name: str) -> Device:
        """
        Get a device by its name.

        Args:
            name (str): Name of the device.

        Returns:
            Device: Device object if found, None otherwise.
        """
        return self.remote.getDevice(name)

    def getBasicTimeStep(self) -> float:
        """
        Get the basic time step of the simulation.

        Returns:
            float: Basic time step value.
        """
        return self.remote.getBasicTimeStep()

    def getName(self) -> str:
        """
        Get the name of the remote.

        Returns:
            str: Name of the remote.
        """
        return self.remote.getName()

    def step(self, time_step):
        """
        Perform a simulation step with the given time step.

        Args:
            time_step (int, optional): Time step in milliseconds. Defaults to None.

        Returns:
            int: Result of the simulation step.
        """
        self.remote.step(time_step)

    def append(self, message: Message):
        """
        Add a message to the list of messages, sorting it based on message priority.

        Args:
            message (Message): The message to append to the list.
        """
        priority = MESSAGE_TYPE_PRIORITY.priority(str(message.message_type))
        index = next((i for i, msg in enumerate(self.list_messages) if MESSAGE_TYPE_PRIORITY.priority(str(msg.message_type)) < priority),
                     len(self.list_messages))
        self.list_messages.insert(index, message)

    def getKeyboard(self):
        """
        Get the keyboard device
        """
        return self.remote.getKeyboard()
