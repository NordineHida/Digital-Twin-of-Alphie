from controller import Robot

# Maximum speed of the robot (NOT DEFINITIVE YET)
MAX_SPEED = 6.28

# Number of motors on each side of the robot
NUM_MOTORS = 5

class MovementManager:
    """
    Manage the movement of the track robot (Forward, backward, right, left and stop moving)
    """
    def __init__(self):
        """
        Initialize the motors.

        This function initializes the left and right motors of the robot.
        It sets their positions to INFINITY and velocities to 0.0.
        """
        self.robot = Robot()
        self.left_motors = [self.robot.getDevice(f"wheel_motor0{i}") for i in range(5)]
        self.right_motors = [self.robot.getDevice(f"wheel_motor1{i}") for i in range(5)]

        for motor in self.left_motors + self.right_motors:
            motor.setPosition(float('inf'))
            motor.setVelocity(0.0)

    def stop(self):
        """
        Stop the robot (set the motor's velocity to 0)

        This function stops the robot by setting the velocity of all motors to 0.0.
        """
        for motor in self.left_motors + self.right_motors:
            motor.setVelocity(0.0)

    def move_forward(self):
        """
        Move the robot forward (at Max_speed)

        This function makes the robot move forward by setting the velocity of all motors to -MAX_SPEED.
        """
        for motor in self.left_motors + self.right_motors:
            motor.setVelocity(-MAX_SPEED)

    def move_left(self):
        """
        Rotate the robot to the left

        This function rotates the robot to the left by setting the velocity of left motors to -MAX_SPEED
        and the velocity of right motors to MAX_SPEED.
        """
        for left_motor, right_motor in zip(self.left_motors, self.right_motors):
            left_motor.setVelocity(-MAX_SPEED)
            right_motor.setVelocity(MAX_SPEED)

    def move_right(self):
        """
        Rotate the robot to the right

        This function rotates the robot to the right by setting the velocity of left motors to MAX_SPEED
        and the velocity of right motors to -MAX_SPEED.
        """
        for left_motor, right_motor in zip(self.left_motors, self.right_motors):
            left_motor.setVelocity(MAX_SPEED)
            right_motor.setVelocity(-MAX_SPEED)

if __name__ == "__main__":
    movement_manager = MovementManager()

