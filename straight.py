#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Reads encoder values and determines correction needed.
'''

__author__ = "Marcello Cierro"
__copyright__ = "Copyright 2018, CSC 436"
__credits__ = ["Landon Patmore","Christian Sumano", "John Santos", "Stephen DiCerce", "Gage Davidson"]
__license__ = "MIT"

import gopigo as go
import sys
import time
import math

'''
Initializations of Constants
'''

encoder_left_init = 0
encoder_right_init = 0

MIN_SPEED = 50
MAX_SPEED = 100


ADDRESS = 0x08
US_CMD = [117]
ENC_CMD = [53]


'''
Overrides GOPIGO enc_reader, provides functionality to read encoder.

Parameters
----------
motor
    The motor on the current rover.
'''
def enc_read(motor):
    go.write_i2c_block(ADDRESS, ENC_CMD+[motor,0,0])
    try:
        b1=go.bus.read_byte(ADDRESS)
        b2=go.bus.read_byte(ADDRESS)
    except IOError:
        return -1
    if b1 != -1 and b2 != -1:
        v = b1*256+b2
        return v
    else:
        return -1

'''
Reads current encoder values and compares the difference with our initial
readings.

Returns
----------
A tuple of the left encoder differential and right encoder differential
'''
def read_encoders():
    encoder_right_reading = enc_read(1)
    encoder_left_reading = enc_read(0)

    left_encoder_differential = encoder_left_reading - encoder_left_init
    right_encoder_differential = encoder_right_reading - encoder_right_init

    return (left_encoder_differential, right_encoder_differential)

'''
Accelerates the rover if the current speed is less than the MAX_SPEED

Parameters
----------
speed
    The speed being compared and manipulated

Returns
----------
Adjusted values to use for correction, depending on the speed at
which we're traveling.
'''
def correctionNeeded(speed):
    if speed > MIN_SPEED:
        #Magic Values, DO NOT TOUCH
        return int((speed)/100) + 11
    else:
        #Magic Values, DO NOT TOUCH
        return int((speed)/100) + 10

'''
Adjusts the left and right motor speeds based on our correction values.

Parameters
----------
speed
    The speed being corrected.
'''
def correctLeft(speed):
    print "Correcting LEFT!"
    go.set_left_speed(speed - correctionNeeded(speed))
    #Corrects wheel size offset by multiplying by 2.
    go.set_right_speed(speed + correctionNeeded(speed)*2)

'''
Adjusts the left and right motor speeds based on our correction values.

Parameters
----------
speed
    The speed being corrected.
'''
def correctRight(speed):
    print "Correcting RIGHT!"
    go.set_left_speed(speed + correctionNeeded(speed))
    go.set_right_speed(speed - correctionNeeded(speed))

'''
Balances our rover when left or right correction is not needed.

Parameters
----------
speed
    The speed being corrected.
'''
def defaultCorrection(speed):
    print "Correcting!"
    go.set_left_speed(speed - correctionNeeded(speed))
    go.set_right_speed(speed + correctionNeeded(speed))

'''
Determines what correction is needed and calls the respective function.

Parameters
----------
left_encoder_differential
    The left encoder difference to be compared to.
right_encoder_differential
    The right encoder difference to be compared to.
speed
    The speed being corrected.
'''
def correctMotors(left_encoder_differential, right_encoder_differential, speed):
    if left_encoder_differential < right_encoder_differential:
        correctRight(speed)
    elif left_encoder_differential > right_encoder_differential:
        correctLeft(speed)
    else:
        defaultCorrection(speed)
'''
Culmination of functions to make the rover go straight. This is achieved by
pulling the current encoder differentials correcting each motor as needed.

Parameters
----------
INIT_LEFT
    Initial left encoder value.
INIT_RIGHT
    Initial right encoder value.
'''
def rs(INIT_LEFT, INIT_RIGHT):
    global encoder_left_init, encoder_right_init
    encoder_left_init = INIT_LEFT
    encoder_right_init = INIT_RIGHT

    current_left_encoder_differential,current_right_encoder_differential = read_encoders()
    print "Current Left Encoder Value: ", current_left_encoder_differential
    print "Current Right Encoder Value: ", current_right_encoder_differential
    correctMotors(current_left_encoder_differential, current_right_encoder_differential, go.read_motor_speed()[1])
