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


#include <stdio.h>
#include <stdlib.h>

#include "e-puck-move_to_destination_location.h"
#include "motor_controller.h"
#include <webots/compass.h>
#include <webots/gps.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include <webots/robot.h>

int time_step;

/*
Method to get simulator time step.
Webots have simulator time step. 
The basic time step is the time step increment used by Webots to advance the virtual time and perform physics simulation.
*/
int getTimeStep()
{
    static int time_step = -1;
    if (time_step == -1)
        time_step = (int)wb_robot_get_basic_time_step();
    return time_step;
}

/*
This command is to perform simulation steps. 
This needed for the controller time step. 
The controller time step is the time increment of time executed at each iteration of the control loop of a controller. 
We must call this to synchronize our program and the simulator condition. 
It will return -1 if the simulation is stopped. 
If we not call this command, the robot will do nothing. 
For example the wb_motor_set_velocity(left_motor, MAX_SPEED) only set the motor speed value. 
So we need to call and looping the wb_robot_step(time_step) command to make the robot move.
*/
void step()
{
    if (wb_robot_step(time_step) == -1)
    {
        wb_robot_cleanup();
        exit(EXIT_SUCCESS);
    }
}

static void init()
{
  time_step = getTimeStep();
  motorControllerInit(time_step);
  step();
}

// Fonction pour obtenir l'angle de cap en degrés
double getBearingInDegrees(WbDeviceTag compass) {
    const double *north = wb_compass_get_values(compass);
    double rad = atan2(north[1], north[0]);
    double bearing = (rad - 1.5708) / M_PI * 180.0;
    if (bearing < 0.0)
        bearing += 360.0;
    printf("Angle du cap de la boussole : %f \n",bearing);
    return bearing;
}

// Fonction pour tourner le robot vers les coordonnées spécifiées
void rotateToDestination(WbDeviceTag compass, double x, double y) {
    const double tolerance = 1;  // Tolérance pour considérer la destination atteinte
    
    // Obtenir les valeurs actuelles de la boussole
    const double *compassValues = wb_compass_get_values(compass);

    // Calculer l'angle actuel de la boussole en radians
    double currentAngleRad = atan2(compassValues[1], compassValues[0]);

    // Calculer l'angle vers la destination en radians
    double angleToDestinationRad = atan2(y, x);

    // Calculer la différence d'angle en radians
    double angleDifferenceRad = angleToDestinationRad - currentAngleRad;

    // Ajuster la différence d'angle pour qu'elle soit dans la plage [-π, π)
    if (angleDifferenceRad < -M_PI)
        angleDifferenceRad += 2.0 * M_PI;
    else if (angleDifferenceRad >= M_PI)
        angleDifferenceRad -= 2.0 * M_PI;

    // Convertir l'angle en degrés
    double angleToDestination = angleDifferenceRad * 180.0 / M_PI;

    // Vérifier la tolérance pour considérer la destination atteinte
    if (fabs(angleToDestination) < tolerance) {
        printf("Angle atteint!\n");
        return;
    }

    // Choisir la direction de rotation en fonction de la différence d'angle
    if (angleToDestination > 0) {
        motorRotateLeft();  // Tourner à gauche
    } else {
        motorRotateRight();  // Tourner à droite
    }

    // Mettre à jour la simulation
    wb_robot_step(32);
    rotateToDestination(compass, x, y);  // Appel récursif pour continuer la rotation
}


void getCurrentPosition(WbDeviceTag gps, double *meX, double *meY) {
    // Obtenir les coordonnées actuelles du GPS
    const double *gpsValues = wb_gps_get_values(gps);
    *meX = gpsValues[0];
    *meY = gpsValues[1]; 
}

void calculateGoTo(double meX, double meY, double cibleX, double cibleY, double *goToX, double *goToY) {
    *goToX = cibleX - meX;
    *goToY = cibleY - meY;
}


void printValues(double meX, double meY, double goToX, double goToY) {
    // Afficher les valeurs
    printf("meX: %.2f, meY: %.2f, goToX: %.2f, goToY: %.2f\n", meX, meY, goToX, goToY);
}

bool isArrived(double currentX, double currentY, double targetX, double targetY) {
    double tolerance = 0.5;
    double differenceX = fabs(currentX - targetX);
    double differenceY = fabs(currentY - targetY);
        
    bool result = differenceX < tolerance && differenceY < tolerance;
   
    return result;
}


void moveForwardWithDuration(double duration) {
    // set robot motor to move forward
    motorMoveForward();

    // run the simulator for the specified duration
    double start_time = wb_robot_get_time();
    do {
        step();
    } while (wb_robot_get_time() < start_time + duration);

    // stop the motor
    motorStop();
    step();
}

int main(int argc, char **argv) {
    wb_robot_init();
    init();
    
    WbDeviceTag compass = wb_robot_get_device("compass");;
    WbDeviceTag gps = wb_robot_get_device("gps");
    wb_gps_enable(gps, 10);
    wb_compass_enable(compass, 10);

    double cibleX = 2.0;
    double cibleY = 2.0;

    double meX, meY, goToX, goToY;

    do
    {
            getCurrentPosition(gps, &meX, &meY);
            calculateGoTo(meX, meY, cibleX, cibleY, &goToX, &goToY);

            printValues(meX, meY, goToX, goToY);

            const double *compassValues = wb_compass_get_values(compass);
            printf("Boussole - X: %.2f, Y: %.2f, Z: %.2f\n", compassValues[0], compassValues[1], compassValues[2]);

            rotateToDestination(compass, goToX, goToY);

            moveForwardWithDuration(10.0);

        // Faire avancer la simulation dans le temps
        wb_robot_step(32); // 32 ms par étape

        getCurrentPosition(gps, &meX, &meY);
        
        sleep(1);
      
    } while (!isArrived(meX, meY, cibleX, cibleY));

    wb_robot_cleanup();
    return 0;
}
