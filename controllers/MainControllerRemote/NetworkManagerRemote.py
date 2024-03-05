"""
File:           NetworkManagerRemote.py
Date:           February 2024
Description:    Manage the network of communication between the remote and robots
Author:         Nordine HIDA
Modifications:
"""

from CommunicationManager import *


class NetworkManagerRemote:
    """
    Manage the network of communication between the remote and robots.
    It sends messages bound to keys and reacts to incoming messages.
    """

    def __init__(self, remote: RobotUpRemote):
        """
        Initialize the NetworkManager.

        Args:
            remote (RobotUpRemote): The remote
        """
        self.remote = remote
        self.robot_name = self.remote.getName()

        self.communication = CommunicationManager(self.remote)

        # Initialize the keyboard
        self.keyboard = self.remote.getKeyboard()
        self.keyboard.enable(10)

    def update(self):
        """
        Check if there is message or a pressed key and handle it.
        """

        # Check if a key is pressed
        key = self.keyboard.getKey()
        if key != -1:
            # Home -> REPORT_BEGIN_ROLLCALL and reset known_robot
            if key == Keyboard.HOME:
                # Set all robots in known_robots to "MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE"
                if self.remote.known_robots is not None:
                    for key in self.remote.known_robots:
                        self.remote.known_robots[key] = MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE
                self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL, 0))
                self.remote.is_callrolling = True

            # END -> STOP
            elif key == Keyboard.END:
                self.communication.send_message_all(self.robot_name, MESSAGE_TYPE_PRIORITY.STOP, 0)

            # Arrow keys -> GO_TO_COORDINATES with different coordinates
            elif key == Keyboard.RIGHT:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, 0, "1:1", self.remote.first_rob))
            elif key == Keyboard.UP:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, 0, "1:-1", self.remote.first_rob))
            elif key == Keyboard.LEFT:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, 0, "-1:1", self.remote.first_rob))
            elif key == Keyboard.DOWN:
                self.communication.send_message(
                    Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, 0, "-1:-1", self.remote.first_rob))

            # Page down -> Path which form a circle around (0;0)
            elif key == Keyboard.PAGEDOWN:
                import math

                # Center of the circle
                center_x = 0
                center_y = 0

                # Radius of the circle
                radius = 1.5

                # Number of points to generate
                num_points = 20

                for i in range(num_points):
                    # Calculate angle for each point
                    angle = 2 * math.pi * i / num_points

                    # Calculate coordinates for each point
                    x = round(center_x + radius * math.cos(angle), 3)
                    y = round(center_y + radius * math.sin(angle), 3)

                    # Sending message to go to coordinates
                    message = Message(self.robot_name, MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES, 0, f"{x}:{y}", self.remote.first_rob)
                    self.communication.send_message(message)

            else:
                # Help menu with all commands and their key
                self.print_help_commands()

        # try to receive a message and add it to the remote's list
        self.communication.receive_message()

        # Check if the list of messages is not empty
        if self.remote.list_messages:
            # Getting the first message and remove it from the list
            message = self.remote.list_messages[0]
            self.remote.list_messages.pop(0)

            id_sender = message.id_sender
            message_type = MESSAGE_TYPE_PRIORITY.from_string(str(message.message_type))
            payload = message.payload

            match message_type:
                case MESSAGE_TYPE_PRIORITY.REPORT_STATUS:
                    self.case_REPORT_STATUS(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_POSITION:
                    self.case_REPORT_POSITION(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
                    self.case_STATUS_GOTOCOORDINATES(id_sender)

                case MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                    self.case_STATUS_FREE(id_sender)

                case MESSAGE_TYPE_PRIORITY.STOP:
                    self.case_STOP()

                case MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES:
                    self.case_GO_TO_COORDINATES(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL:
                    self.case_REPORT_BEGIN_ROLLCALL(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE:
                    self.case_STATUS_OUT_RANGE(payload)

                case _:
                    print("Unknown message received")

            self.update_first_rob()

    def update_first_rob(self):
        """
        Update first_rob by retrieving the first robot in alphabetical order
        with value "STATUS_FREE". If none found, set to None.
        """
        # Get the keys of known_robots sorted alphabetically
        sorted_keys = sorted(self.remote.known_robots.keys())

        # Set initial value of first_rob to ""
        self.remote.first_rob = ""

        # Iterate through the sorted keys
        i = 0
        while i < len(sorted_keys) and self.remote.first_rob == "":
            key = sorted_keys[i]
            # Check if the value of the key is "STATUS_FREE"
            if self.remote.known_robots[key] == str(MESSAGE_TYPE_PRIORITY.STATUS_FREE):
                # Update first_rob with the robot's name
                self.remote.first_rob = key
            i += 1

    def case_REPORT_STATUS(self, id_sender, payload):
        # TODO: Implement handling of REPORT_STATUS message
        pass

    def case_REPORT_POSITION(self, id_sender, payload):
        # TODO: Implement handling of REPORT_POSITION message
        pass

    def case_STATUS_GOTOCOORDINATES(self, id_sender):
        self.remote.known_robots[id_sender] = MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES

    def case_STATUS_FREE(self, id_sender):
        self.remote.known_robots[id_sender] = MESSAGE_TYPE_PRIORITY.STATUS_FREE

    def case_STOP(self):
        # TODO: Implement handling of STOP message
        pass

    def case_GO_TO_COORDINATES(self, id_sender, payload):
        # TODO: Implement handling of GO_TO_COORDINATES message
        pass

    def case_REPORT_BEGIN_ROLLCALL(self, id_sender, payload):
        if id_sender != "Initializer":
            self.remote.known_robots[id_sender] = payload

    def case_STATUS_OUT_RANGE(self, payload: str):
        """
        Get the complete list of robots in the simulation and add it to the remote's known_robot
        Args:
            payload (str): The payload of the message composed of all remote's name concatenated and separated by a ':'.
        """
        all_known_robots = payload.split(":")
        self.remote.known_robots = {name: MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE for name in all_known_robots}

    @staticmethod
    def print_help_commands():
        """
        Print all commands and their keys
        """
        print("------------------------------------------ COMMANDS ---------------------------------------")
        print("Any key     : Show all commands")
        print("\n")
        print("HOME        : Call the roll (should be used before any tasks)")
        print("END         : Stop everything and reset robot's data ")
        print("\n")
        print("PAGEDOWN    : Go to coordinates (Circle around the (0;0)) ")
        print("RIGHT       : Go to coordinates (1;1) ")
        print("LEFT        : Go to coordinates (-1;1) ")
        print("UP          : Go to coordinates (1;-1) ")
        print("DOWN        : Go to coordinates (-1;-1) ")
        print("-------------------------------------------------------------------------------------------")
