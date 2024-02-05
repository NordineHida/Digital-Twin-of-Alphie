/*
 * Copyright 2021 Albert Alfrianta
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * 
 * Created on: 2021-08, Bogor, Indonesia
 * 
 * Contact: albert.alfrianta@gmail.com or https://www.linkedin.com/in/albert-alfrianta/
 * 
 * Description:
 * 	Please read the header file for the method explanations.
 */


#include "motor_controller.h"

#include <webots/robot.h>
#include <webots/motor.h>

#define MAX_SPEED 6.28 //angular speed in rad/s
static WbDeviceTag left_motor_0,left_motor_1,left_motor_2,left_motor_3,left_motor_4,
right_motor_5,right_motor_6,right_motor_7,right_motor_8,right_motor_9;

void motorControllerInit(int time_step)
{
    // get a handler to the motors and set target position to infinity (speed control).
    left_motor_0 = wb_robot_get_device("wheel_motor00");
    right_motor_5 = wb_robot_get_device("wheel_motor05");
    left_motor_1 = wb_robot_get_device("wheel_motor01");
    right_motor_6 = wb_robot_get_device("wheel_motor06");
    left_motor_2 = wb_robot_get_device("wheel_motor02");    
    right_motor_7 = wb_robot_get_device("wheel_motor07");
    left_motor_3 = wb_robot_get_device("wheel_motor03");
    right_motor_8 = wb_robot_get_device("wheel_motor08");
    left_motor_4 = wb_robot_get_device("wheel_motor04");
    right_motor_9 = wb_robot_get_device("wheel_motor09");


    wb_motor_set_position(left_motor_0, INFINITY);
    wb_motor_set_position(left_motor_1, INFINITY);
    wb_motor_set_position(left_motor_2, INFINITY);
    wb_motor_set_position(left_motor_3, INFINITY);
    wb_motor_set_position(left_motor_4, INFINITY);

    wb_motor_set_position(right_motor_5, INFINITY);
    wb_motor_set_position(right_motor_6, INFINITY);
    wb_motor_set_position(right_motor_7, INFINITY);
    wb_motor_set_position(right_motor_8, INFINITY);
    wb_motor_set_position(right_motor_9, INFINITY);

    wb_motor_set_velocity(left_motor_0, 0.0);
    wb_motor_set_velocity(left_motor_1, 0.0);
    wb_motor_set_velocity(left_motor_2, 0.0);
    wb_motor_set_velocity(left_motor_3, 0.0);
    wb_motor_set_velocity(left_motor_4, 0.0);

    wb_motor_set_velocity(right_motor_5, 0.0);
    wb_motor_set_velocity(right_motor_6, 0.0);
    wb_motor_set_velocity(right_motor_7, 0.0);
    wb_motor_set_velocity(right_motor_8, 0.0);
    wb_motor_set_velocity(right_motor_9, 0.0);

}

void motorStop()
{
    wb_motor_set_velocity(left_motor_0, 0.0);
    wb_motor_set_velocity(left_motor_1, 0.0);
    wb_motor_set_velocity(left_motor_2, 0.0);
    wb_motor_set_velocity(left_motor_3, 0.0);
    wb_motor_set_velocity(left_motor_4, 0.0);

    wb_motor_set_velocity(right_motor_5, 0.0);
    wb_motor_set_velocity(right_motor_6, 0.0);
    wb_motor_set_velocity(right_motor_7, 0.0);
    wb_motor_set_velocity(right_motor_8, 0.0);
    wb_motor_set_velocity(right_motor_9, 0.0);
}

void motorMoveForward()
{

    wb_motor_set_velocity(left_motor_0,  -MAX_SPEED);
    wb_motor_set_velocity(right_motor_5, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_1,  -MAX_SPEED);
    wb_motor_set_velocity(right_motor_6, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_2,  -MAX_SPEED);
    wb_motor_set_velocity(right_motor_7, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_3,  -MAX_SPEED);
    wb_motor_set_velocity(right_motor_8, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_4,  -MAX_SPEED);
    wb_motor_set_velocity(right_motor_9, -MAX_SPEED);
}

void motorRotateLeft()
{
    wb_motor_set_velocity(left_motor_0, -MAX_SPEED);
    wb_motor_set_velocity(right_motor_5, MAX_SPEED);
    wb_motor_set_velocity(left_motor_1, -MAX_SPEED);
    wb_motor_set_velocity(right_motor_6, MAX_SPEED);        
    wb_motor_set_velocity(left_motor_2, -MAX_SPEED);
    wb_motor_set_velocity(right_motor_7, MAX_SPEED);
    wb_motor_set_velocity(left_motor_3, -MAX_SPEED);
    wb_motor_set_velocity(right_motor_8, MAX_SPEED);   
    wb_motor_set_velocity(left_motor_4, -MAX_SPEED);
    wb_motor_set_velocity(right_motor_9, MAX_SPEED);
 
}

void motorRotateRight()
{
    wb_motor_set_velocity(left_motor_0, MAX_SPEED);
    wb_motor_set_velocity(right_motor_5, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_1, MAX_SPEED);
    wb_motor_set_velocity(right_motor_6, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_2, MAX_SPEED);
    wb_motor_set_velocity(right_motor_7, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_3, MAX_SPEED);
    wb_motor_set_velocity(right_motor_8, -MAX_SPEED);
    wb_motor_set_velocity(left_motor_4, MAX_SPEED);
    wb_motor_set_velocity(right_motor_9, -MAX_SPEED);   
}