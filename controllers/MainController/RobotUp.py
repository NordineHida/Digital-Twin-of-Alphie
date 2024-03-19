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

        # Range of the emitter (CAN BE MODIFIED)
        self.range_emitter = 5
        # the maximum number of times that a message can be shared (CAN BE MODIFIED)
        self.max_counter = 4

        # boolean to know if the known_robots list has been initialized by the initializer.
        self.is_initialized = False

        # current task of the robot (free by default)
        self.robot_current_task = MESSAGE_TYPE_PRIORITY.STATUS_FREE

        # list of all robots + self (initialized by the initializer)
        self.known_robots = None

        # dictionary of nearby robots and the last time I received a communication from it (updated in networkManager)
        self.neighbors_last_com = None

        # Next and previous known robot in alphabetical order
        self.next_rob = None
        self.prev_rob = None

        # first free robot in the known list
        self.first_free_rob = None

        # boolean to remember if the robot has already call rolled
        self.is_callrolling = False

        # List of next coordinates
        self.next_coordinates: List[Coordinates] = []

        # boolean to know if the robot has been stopped
        self.is_stopped = False

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

    def reset(self):
        """
        Reset all data collected by the robot
        """
        # Clear the list of messages
        self.list_messages.clear()

        # Reset robot_current_task to default value
        self.robot_current_task = MESSAGE_TYPE_PRIORITY.STATUS_FREE

        self.reset_known_robot()

        # Reset prev, next and free rob to None
        self.prev_rob = None
        self.next_rob = None
        self.first_free_rob = None

        # Reset is_callrolling flag
        self.is_callrolling = False

        # Clear the list of next coordinates
        self.next_coordinates.clear()

    def reset_known_robot(self):
        """
        Set all robots in known_robots to "MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE"
        """
        if self.known_robots is not None:
            for key in self.known_robots:
                self.known_robots[key] = MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE
