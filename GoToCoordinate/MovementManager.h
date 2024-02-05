#ifndef MOVEMENT_MANAGER_H
#define MOVEMENT_MANAGER_H

/*
 * File:          MovementManager.h
 * Date:          February 2024
 * Description:   Header file for managing the movement of the track robot (Forward, backward, right, left, and stop moving)
 * Author:        Nordine HIDA
 * Modifications:
 */

#include <webots/robot.h>
#include <webots/motor.h>

 // Maximum speed of the robot (NOT DEFINITIVE YET)
#define MAX_SPEED 6.28

// Number of motors on each side of the robot
#define NUM_MOTORS 5

// Arrays to store WbDeviceTag for left and right motors
extern WbDeviceTag left_motors[NUM_MOTORS];
extern WbDeviceTag right_motors[NUM_MOTORS];

/*
 * Initialize the motors
 *
 * This function initializes the left and right motors of the robot.
 * It sets their positions to INFINITY and velocities to 0.0.
 */
void MoveInit();

/*
 * Stop the robot (set the motor's velocity to 0)
 *
 * This function stops the robot by setting the velocity of all motors to 0.0.
 */
void MoveStop();

/*
 * Move the robot forward (at Max_speed)
 *
 * This function makes the robot move forward by setting the velocity of all motors to -MAX_SPEED.
 */
void MoveForward();

/*
 * Rotate the robot to the left
 *
 * This function rotates the robot to the left by setting the velocity of left motors to -MAX_SPEED
 * and the velocity of right motors to MAX_SPEED.
 */
void MoveLeft();

/*
 * Rotate the robot to the right
 *
 * This function rotates the robot to the right by setting the velocity of left motors to MAX_SPEED
 * and the velocity of right motors to -MAX_SPEED.
 */
void MoveRight();

#endif
