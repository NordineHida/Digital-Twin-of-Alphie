"""
File:          MovementManager.py
Date:          February 2024
Description:   Manage the movement of the track robot (Forward, backward, right, left and stop moving)
Author:        Nordine HIDA
Modifications:
"""

# CONSTANTS
# Maximum speed of the robot (NOT DEFINITIVE YET)
MAX_SPEED = 6.28

# Number of motors on each side of the robot
NUM_MOTORS = 5


class MovementManager:
    """
    Manage the movement of the track robot (Forward, backward, right, left and stop moving)
    """

    def __init__(self, robot):
        """
        Initializes the left and right motors of the robot.
        """
        self.robot = robot
        self.right_motors = [self.robot.getDevice(f"wheel_motor0{i}") for i in range(5)]
        self.left_motors = [self.robot.getDevice(f"wheel_motor0{i+5}") for i in range(5)]

        for motor in self.left_motors + self.right_motors:
            motor.setPosition(float('inf'))
            motor.setVelocity(0.0)

    def stop(self):
        """
        Stop the robot (set the motor's velocity to 0)
        """
        for motor in self.left_motors + self.right_motors:
            motor.setVelocity(0.0)

    def move_forward(self):
        """
        Move the robot forward (at Max_speed)
        """
        for motor in self.left_motors + self.right_motors:
            motor.setVelocity(-MAX_SPEED)

    def move_left(self):
        """
        Rotate the robot to the left by setting the velocity of left motors to MAX_SPEED
        and the velocity of right motors to -MAX_SPEED.
        """
        for left_motor in self.left_motors:
            left_motor.setVelocity(-MAX_SPEED)

        for right_motor in self.right_motors:
            right_motor.setVelocity(MAX_SPEED)

    def move_right(self):
        """
        Rotate the robot to the right by setting the velocity of left motors to MAX_SPEED
        and the velocity of right motors to -MAX_SPEED.
        """
        for left_motor in self.left_motors:
            left_motor.setVelocity(MAX_SPEED)

        for right_motor in self.right_motors:
            right_motor.setVelocity(-MAX_SPEED)
