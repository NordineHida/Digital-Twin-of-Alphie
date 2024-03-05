"""
File:           RobotUpInitializer.py
Date:           February 2024

Description:    This involves overriding Webots' robot class with additional attributes,
                such as a list of messages to process. However, it is specifically designed for the initializer
                remote, which retrieves all active robots at the beginning of the simulation and distributes this
                information to all robots. This is aimed at providing all robots with awareness of their environment
                (i.e., all robots in the network), even though this list can be altered during the simulation.

Author:         Nordine HIDA
Modifications:
"""

from controller import Supervisor
from controller.robot import *
from Message import *
from typing import List


class RobotUpInitializer:
    """
    RobotUp class overrides the webots Robot class with additional attributes and methods.
    """

    def __init__(self):
        """
        Constructor for RobotUp class. Init all attributes
        """
        self.robot = Supervisor()
        self.list_messages: List[Message] = []

        # list of all robots
        self.known_robots = {}

        # boolean to remember if the robot has already call rolled
        self.is_callrolling = False

    def getNumberOfRobots(self) -> int:
        """
        Get the number of robots in the simulation.
        |!| (WITHOUT THE INITIALIZER AND THE REMOTE)

        Returns:
            int: Number of robots in the simulation.
        """
        root_node = self.robot.getRoot()
        if not root_node:
            print("Error: Root node is None.")
            return 0

        children = root_node.getField('children')
        if not children:
            print("Error: Children nodes are None.")
            return 0

        number_of_robots = 0
        for i in range(children.getCount()):
            child_node = children.getMFNode(i)
            if child_node.getTypeName() == "Robot":
                number_of_robots += 1
        return number_of_robots - 2

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
