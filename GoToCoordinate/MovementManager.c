/*
 * File:          MovementManager.c
 * Date:          February 2024
 * Description:   Manage the movement of the track robot (Forward, backward, right, left and stop moving)
 * Author:        Nordine HIDA
 * Modifications:
 */

#include <webots/robot.h>
#include <webots/motor.h>

#define MAX_SPEED 6.28  // Max speed of the robot (NOT DEFINITIVE YET)
#define NUM_MOTORS 5    // number of motors on each side of the robot

// Arrays to store WbDeviceTag for left and right motors
static WbDeviceTag left_motors[NUM_MOTORS], right_motors[NUM_MOTORS];

/*
 * Initialize the motors
 */
void MoveInit() 
{
    const char* right_motor_names[NUM_MOTORS] = { "wheel_motor00", "wheel_motor01", "wheel_motor02", "wheel_motor03", "wheel_motor04" };
    const char* left_motor_names[NUM_MOTORS] = { "wheel_motor05", "wheel_motor06", "wheel_motor07", "wheel_motor08", "wheel_motor09" };

    // Loop through each motor and initialize
    for (int i = 0; i < NUM_MOTORS; ++i) {
        // Get motor devices by their tag (you can found it on the "device" node in webots)
        left_motors[i] = wb_robot_get_device(left_motor_names[i]);
        right_motors[i] = wb_robot_get_device(right_motor_names[i]);

        // Initialize position
        wb_motor_set_position(left_motors[i], INFINITY);
        wb_motor_set_position(right_motors[i], INFINITY);

        // Initialize velocity
        wb_motor_set_velocity(left_motors[i], 0.0);
        wb_motor_set_velocity(right_motors[i], 0.0);
    }
}

/*
 * Stop the robot (set the motor's velocity to 0)
 */
void MoveStop() 
{
    // Loop through each motor and set velocity to 0
    for (int i = 0; i < NUM_MOTORS; ++i) {
        wb_motor_set_velocity(left_motors[i], 0.0);
        wb_motor_set_velocity(right_motors[i], 0.0);
    }
}

/*
 * Move the robot forward (at Max_speed)
 */
void MoveForward() 
{
    // Loop through each motor and set velocity to -MAX_SPEED
    for (int i = 0; i < NUM_MOTORS; ++i) {
        wb_motor_set_velocity(left_motors[i], -MAX_SPEED);
        wb_motor_set_velocity(right_motors[i], -MAX_SPEED);
    }
}

/*
 * Rotate the robot to the left
 */
void MoveLeft() 
{
    // Loop through each motor and set velocity accordingly for left rotation
    for (int i = 0; i < NUM_MOTORS; ++i) {
        wb_motor_set_velocity(left_motors[i], -MAX_SPEED);
        wb_motor_set_velocity(right_motors[i], MAX_SPEED);
    }
}

/*
 * Rotate the robot to the right
 */
void MoveRight() 
{
    // Loop through each motor and set velocity accordingly for right rotation
    for (int i = 0; i < NUM_MOTORS; ++i) {
        wb_motor_set_velocity(left_motors[i], MAX_SPEED);
        wb_motor_set_velocity(right_motors[i], -MAX_SPEED);
    }
}
