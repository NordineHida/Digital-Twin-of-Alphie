"""
File:           NetworkManager.py
Date:           February 2024
Description:    Manage the network of communication between robots,
                facilitating the retrieval of nearby robots and
                determining which ones should take action.
Author:         Nordine HIDA
Modifications:
"""

from MovementManager import *
from CommunicationManager import *


class NetworkManager:
    """
    Manage the network of communication between robots,
    facilitating the retrieval of nearby robots and
    determining which ones should take action.
    """

    def __init__(self, robot: RobotUp):
        """
        Initialize the NetworkManager.

        Args:
            robot (RobotUp): The robot
        """
        self.robot = robot
        self.robot_name = self.robot.getName()

        # Communication manager
        self.communication = CommunicationManager(self.robot)
        self.movement = MovementManager(self.robot)

        self.compteur = 0

    def go_to_coordinates(self, x: float, y: float):
        """
        If the robot is free, call the task to move the robot to coordinates
        else it adds those coordinates to its list of next coordinates

        When it reaches its goal, it sends a message to tell that it is free and where it stopped.
        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        """
        import Task_GoToCoordinates as GTC

        # if i'm free I move
        if self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
            self.robot.robot_current_task = str(MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES) + ":" + str(x) + ":" + str(y)
            GTC.go_to_coordinates(self.robot, Coordinates(float(x), float(y)))

            # Here the robot has reached its goal, or it has been stopped -> Status free.
            self.robot.robot_current_task = MESSAGE_TYPE_PRIORITY.STATUS_FREE

            # If it hasn't been stopped, it sends a message to the first free robot to tell where it should go.
            if not self.robot.is_stopped:
                self.update_prev_next_firstfree_robot()
                recipient = ""
                if self.robot.first_free_rob:
                    recipient = self.robot.first_free_rob
                self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.STATUS_FREE, 0,
                                                        f"{MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES}:{x}:{y}",
                                                        recipient))

        # if I'm already moving, I add new Coordinates to move
        elif self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
            self.robot.next_coordinates.append(Coordinates(float(x), float(y)))

    def case_REPORT_STATUS(self, id_sender: str, payload: str):
        """
        Handle the REPORT_STATUS message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        # TODO: Handle the REPORT_STATUS message
        pass

    def case_REPORT_POSITION(self, id_sender: str, payload: str):
        """
        Handle the REPORT_POSITION message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        # TODO: Handle the REPORT_POSITION message
        pass

    def case_STATUS_GOTOCOORDINATES(self, id_sender: str, payload: str):
        """
        Handle the STATUS_GOTOCOORDINATES message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        # TODO: Handle the STATUS_GOTOCOORDINATES message
        pass

    def case_STATUS_FREE(self, id_sender: str, payload: str) -> int:
        """
        Handle the STATUS_FREE message.
        It sets the sender as a STATUS_FREE and react according the context.
        (See "If" description for more information)

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.

        Returns:
            int: An integer indicating the action to take. If the STATUS_FREE message should be considered
                 as a STOP message, it returns STOP.value
                 otherwise, it returns STATUS_FREE.value
        """
        context_value = MESSAGE_TYPE_PRIORITY.STATUS_FREE.value
        if payload != "STOP":
            # Sets the sender as a STATUS_FREE
            self.robot.known_robots[id_sender] = MESSAGE_TYPE_PRIORITY.STATUS_FREE

        # If the previous robot just finished going to coordinates, I follow it
        if payload.startswith(str(MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES)):
            msg, x, y = payload.split(":")
            if self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                self.go_to_coordinates(float(x), float(y))
            else:
                self.robot.next_coordinates.append(Coordinates(float(x), float(y)))

        # If self robot is already on its way to coordinates, check if the sender has already been there
        elif str(self.robot.robot_current_task).startswith(str(MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES)):
            msg, x, y = payload.split(":")
            me_msg, me_x, me_y = str(self.robot.robot_current_task).split(":")
            # If a robot has already reached my coordinates, I stop myself
            if x == me_x and y == me_y:
                self.movement.stop()
                context_value = MESSAGE_TYPE_PRIORITY.STOP.value

        # If the payload is STOP, execute the case_STOP
        elif payload == "STOP":
            self.case_STOP(id_sender, payload)

        return context_value

    def case_STOP(self, send_counter: int):
        """
        Stop the robot movement and reset it.
        Clear all messages, coordinates, known_robot in the robot's memory
        Args:
            send_counter (int): The number of time that this roll call as been sent.
        """
        self.movement.stop()

        # if I'm not already stopped, I send a stop message
        if not self.robot.is_stopped:
            self.communication.send_message(Message(self.robot_name, MESSAGE_TYPE_PRIORITY.STOP, send_counter, "STOP"))

        self.robot.reset()
        self.robot.is_stopped = True

    def case_GO_TO_COORDINATES(self, id_sender: str, payload: str):
        """
        Handle the GO_TO_COORDINATES message.

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
        """
        self.robot.is_stopped = False

        x, y = payload.split(":")
        if self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
            self.go_to_coordinates(float(x), float(y))
        else:
            self.robot.next_coordinates.append(Coordinates(float(x), float(y)))

    def case_REPORT_BEGIN_ROLLCALL(self, id_sender: str, payload: str, send_counter: int):
        """
        Add the sender to It's known list of robot and send the message if the counter hasn't reached the max.
        |!| I RESET MY KNOWN ROBOT IF THE COUNTER = 0 (first iteration of the message)

        Args:
            id_sender (str): The ID of the sender.
            payload (str): The payload of the message.
            send_counter (int): The number of time that this roll call as been sent.
        """

        # unstopped the robot
        self.robot.is_stopped = False
        # If it's the first iteration of the message, I reset the list of known robot to forget old neighbor
        if send_counter == 0:
            self.robot.reset_known_robot()

        message_rollcall = Message(self.robot_name, MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL, send_counter, str(self.robot.robot_current_task))

        # I add the sender if It's a robot and if I'm initialized (= my list of all robots has been filled)
        if self.robot.is_initialized:
            if id_sender != "Remote" and id_sender != "Initializer":
                self.robot.known_robots[id_sender] = payload

        # if the counter hasn't reached the max, I send the message
        if send_counter < self.robot.max_counter:
            self.communication.send_message(message_rollcall)

    def case_STATUS_OUT_RANGE(self, payload: str):
        """
        Get the complete list of robots in the simulation and add it to the robot's known_robot
        Then reset the range of the robot's emitter to the range_emitter value. (Check RobotUp to modify it)
        Args:
            payload (str): The payload of the message composed of all robot's name concatenated and separated by a ':'.
        """
        all_known_robots = payload.split(":")
        self.robot.reset()
        self.communication.clear_messages()
        self.robot.known_robots = {name: MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE for name in all_known_robots}
        self.robot.getDevice("emitter").setRange(self.robot.range_emitter)

        self.robot.is_initialized = True

    def update(self) -> int:
        """
        Handle the received message.

        Returns:
            int : case that was executed (-1 if no messages was handled)
        """
        case_executed = -1

        # try to receive a message and add it to the robot's list
        self.communication.receive_message()

        # Check if the list of messages is not empty
        if self.robot.list_messages:

            # Getting the first message and remove it from the list
            message = self.robot.list_messages[0]
            self.robot.list_messages.pop(0)

            id_sender = message.id_sender
            message_type = MESSAGE_TYPE_PRIORITY.from_string(message.message_type)
            send_counter = message.send_counter
            payload = message.payload

            case_executed = message_type.value

            match message_type:
                case MESSAGE_TYPE_PRIORITY.REPORT_STATUS:
                    self.case_REPORT_STATUS(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_POSITION:
                    self.case_REPORT_POSITION(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_GOTOCOORDINATES:
                    self.case_STATUS_GOTOCOORDINATES(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STATUS_FREE:
                    case_executed = self.case_STATUS_FREE(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.STOP:
                    self.case_STOP(send_counter)

                case MESSAGE_TYPE_PRIORITY.GO_TO_COORDINATES:
                    self.case_GO_TO_COORDINATES(id_sender, payload)

                case MESSAGE_TYPE_PRIORITY.REPORT_BEGIN_ROLLCALL:
                    self.case_REPORT_BEGIN_ROLLCALL(id_sender, payload, send_counter)

                case MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE:
                    self.case_STATUS_OUT_RANGE(payload)

                case _:
                    print("Unknown message received")
                    pass

        if self.robot.next_coordinates and self.robot.robot_current_task == MESSAGE_TYPE_PRIORITY.STATUS_FREE:
            x = self.robot.next_coordinates[0].x
            y = self.robot.next_coordinates[0].y
            self.robot.next_coordinates.pop(0)
            self.go_to_coordinates(x, y)

        if self.robot.is_initialized:
            self.update_prev_next_firstfree_robot()

            if self.compteur > 100:
                print("-----------------------------------", self.robot.getName(), " :  IT KNOWS ----------------------------")
                for key, value in self.robot.known_robots.items():
                    print(f"{key}: {value}")
                print("NEXT :", self.robot.next_rob)
                print("PREV :", self.robot.prev_rob)
                print("FIRST FREE :", self.robot.first_free_rob)
                print("IS CALLROLLING : ", self.robot.is_callrolling)
                print("IS STOPPED : ", self.robot.is_stopped)
                print("IS Initialized : ", self.robot.is_initialized)
                print("-----------------------------------", self.robot.getName(), "------------------------------------- \n ")
                self.compteur = 0
            else:
                self.compteur += 1

        return case_executed

    def update_prev_next_firstfree_robot(self):
        """
        Update the previous, next and the first free robots based on the robot's name and known_robots dictionary.
        |!| It ignores OUT_RANGE robots !

        This method looks into the known_robots dictionary to find the key (robot name) just before and just after
        the current robot's name (self.robot_name). It then updates the prev_rob and next_rob attributes accordingly.

        Then it iterates through the dictionary to find the first available robot (or leaves it as None if no robots are free).
        """
        sorted_robots = sorted(self.robot.known_robots.keys())
        current_index = sorted_robots.index(self.robot_name)

        # Find previous robot ignoring STATUS_OUT_RANGE robots
        prev_index = current_index - 1
        while prev_index >= 0:
            if self.robot.known_robots[sorted_robots[prev_index]] != MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE:
                self.robot.prev_rob = sorted_robots[prev_index]
                break
            prev_index -= 1
        else:
            self.robot.prev_rob = None

        # Find next robot ignoring STATUS_OUT_RANGE robots
        next_index = current_index + 1
        while next_index < len(sorted_robots):
            if self.robot.known_robots[sorted_robots[next_index]] != MESSAGE_TYPE_PRIORITY.STATUS_OUT_RANGE:
                self.robot.next_rob = sorted_robots[next_index]
                break
            next_index += 1
        else:
            self.robot.next_rob = None

        self.robot.first_free_rob = None
        sorted_known_robots = dict(sorted(self.robot.known_robots.items()))
        # Iterate through the sorted robots to get the first free robot
        i = 0
        while i < len(sorted_known_robots) and self.robot.first_free_rob is None:
            key = sorted_robots[i]
            # Check if the value of the key is "STATUS_FREE"
            if sorted_known_robots[key] == str(MESSAGE_TYPE_PRIORITY.STATUS_FREE):
                # Update first_rob with the robot's name
                self.robot.first_free_rob = key
            i += 1
