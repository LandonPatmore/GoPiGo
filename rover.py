#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
State machine controller
"""

__author__ = "Landon Patmore"
__copyright__ = "Copyright 2018, CSC 436"
__credits__ = ["Marcello Cierro","Christian Sumano", "John Santos", "Stephen DiCerce", "Gage Davidson"]
__license__ = "MIT"

import gopigo as go
import sys
import time
import straight as rs

'''
Globals:
--------
STOP_DISTANCE: int
    The distance the rover will stop at
DISTANCE_TO_SLOW: int
    The distance the rover will start to slow
MIN_SPEED: int
    The minimum speed the rover will move
MAX_SPEED: int
    The maximum speed the rover will
CURR_DIST: int
    The distance to the object ahead
STATE: int
    The current state of the rover

'''
STOP_DISTANCE = input('Enter stop distance: ')
DISTANCE_TO_SLOW = input('Enter distance to slow down: ')
MIN_SPEED = 50
MAX_SPEED = 100
CURR_DIST = 0
STATE = 0

'''
Constants:
-------------
STATE:
    0 - Normal
    1 - Slowing Down
    2 - Speeding Up
    3 - Stop

Motors:
    0 - Right motor
    1 - Left motor

Encoders:
    0 - Left encoder
    1 - Right encoder
'''

'''
Checks the distance between the rover and the obstacle ahead and changes the state based on the distance to the obstacle
'''
def checkDistance():
    global STATE
    print("Current distance to obstacle: ", distanceToObstacle())
    if distanceToObstacle() <= STOP_DISTANCE:
        print('STATE: STOP')
        STATE = 3
    elif distanceToObstacle() <= DISTANCE_TO_SLOW:
        print('STATE: SLOW DOWN')
        STATE = 1
    elif (distanceToObstacle() > DISTANCE_TO_SLOW) and (getCurrentSpeed() < MAX_SPEED):
        print('STATE: SPEED UP')
        STATE = 2
    else:
        print('STATE: NORMAL')
        STATE = 0

'''
Checks the current state of the rover and runs the function based on the current state
'''
def stateCheck():
    checkDistance()
    if STATE == 1:
        slowing()
    elif STATE == 2:
        accelerating()
    elif STATE == 3:
        stopped()

'''
Slows the rover down if the current speed is above the MIN_SPEED
'''
def slowing():
    if(getCurrentSpeed() >= MIN_SPEED):
        go.set_speed(getCurrentSpeed() - 5)
    else:
        global STATE
        STATE = 0

'''
Accelerates the rover if the current speed is less than the MAX_SPEED
'''
def accelerating():
    if(getCurrentSpeed() < MAX_SPEED):
        go.set_speed(getCurrentSpeed() + 15)
    else:
        global STATE
        STATE = 0

'''
Stops the rover and sets the speed of the motors to be 0
'''
def stopped():
    go.set_speed(MIN_SPEED)
    go.stop()

'''
Gets the distance to the obstacle in front of the rover

Returns:
--------
Current distance to the obstacle ahead
'''
def distanceToObstacle():
    global CURR_DIST
    dist = go.us_dist(15)
    if(dist != 0):
        CURR_DIST = dist
    return CURR_DIST

'''
Gets the current speed of the rover from the left motor

Returns:
--------
Motor speed
'''
def getCurrentSpeed():
    return go.read_motor_speed()[1]

'''
Reads the current encoder values

Returns:
--------
Left and right encoder values
'''
def read_encoders():
    return (go.enc_read(0), go.enc_read(1))

'''
Main program loop
'''
def main():
    go.set_speed(MIN_SPEED)

    INIT_LEFT_ENC, INIT_RIGHT_ENC = read_encoders()
    print('Left:    ', INIT_LEFT_ENC, ' Right:    ', INIT_RIGHT_ENC)
    time.sleep(5)

    go.forward()
    while True:
        try:
            if STATE == 3:
                go.stop()
            else:
                go.forward()
            print 'MOTORS: ', go.read_motor_speed()
            rs.rs(INIT_LEFT_ENC, INIT_RIGHT_ENC)
            stateCheck()

        # Shuts the ACC down when a Ctrl + c command is issued
        except KeyboardInterrupt:
            print '\nACC shut off'
            go.stop()
            sys.exit()

if __name__ == "__main__":
    main()
