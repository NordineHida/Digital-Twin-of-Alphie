"""
File:           RobotUp.py
Date:           February 2024
Description:    Override of webots's robot with extra attributes, like a list of messages to process
Author:         Nordine HIDA
Modifications:
"""

from controller.robot import *
from Message import *
from Coordinates import *
from typing import List


class RobotUp:
    """
    RobotUp class overrides the webots Robot class with additional attributes and methods.
    """

    def __init__(self):
        """
        Constructor for RobotUp class. Init all attributes
        """
        self.robot = Robot()
        self.list_messages: List[Message] = []

        # Range of the emitter (can be modified)
        self.range_emitter = 1.5

        # boolean to know if the known_robots list has been initialized by the initializer.
        self.is_initialized = False

        # current task of the robot (free by default)
        self.robot_current_task = MESSAGE_TYPE_PRIORITY.STATUS_FREE

        # list of nearby robots + self (initialized by the initializer)
        self.known_robots = None
        self.next_rob = None
        self.prev_rob = None

        # boolean to remember if the robot has already call rolled
        self.is_callrolling = False

        # List of next coordinates
        self.next_coordinates: List[Coordinates] = []

    def getDevice(self, name: str) -> Device:
        """
        Get a device by its name.

        Args:
            name (str): Name of the device.

        Returns:
            Device: Device object if found, None otherwise.
        """
        return self.robot.getDevice(name)

    def getBasicTimeStep(self) -> float:
        """
        Get the basic time step of the simulation.

        Returns:
            float: Basic time step value.
        """
        return self.robot.getBasicTimeStep()

    def getName(self) -> str:
        """
        Get the name of the robot.

        Returns:
            str: Name of the robot.
        """
        return self.robot.getName()

    def step(self, time_step):
        """
        Perform a simulation step with the given time step.

        Args:
            time_step (int, optional): Time step in milliseconds. Defaults to None.

        Returns:
            int: Result of the simulation step.
        """
        self.robot.step(time_step)

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
        return self.robot.getKeyboard()