import gopigo as go
import sys
import time
import math


encoder_left_init = 0
encoder_right_init = 0

MIN_SPEED = 50
MAX_SPEED = 100


ADDRESS = 0x08
US_CMD = [117]
ENC_CMD = [53]

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

def read_encoders():
    encoder_right_reading = enc_read(1)
    encoder_left_reading = enc_read(0)
    print 'leftttttttttttttt', enc_read(0)
    
    left_encoder_differential = encoder_left_reading - encoder_left_init
    right_encoder_differential = encoder_right_reading - encoder_right_init

    return (left_encoder_differential, right_encoder_differential)

def correctionNeeded(speed):
    if speed > MIN_SPEED:
        return int((speed)/100) + 11
    else:
        return int((speed)/100) + 10

def getCurrentSpeed():
    print("Current Speed: "), go.read_motor_speed()
    return go.read_motor_speed()

def correctLeft(speed):
    print "Correcting LEFT!"
    go.set_left_speed(speed - correctionNeeded(speed))
    go.set_right_speed(speed + correctionNeeded(speed)*2)

def correctRight(speed):
    print "Correcting RIGHT!"
    go.set_left_speed(speed + correctionNeeded(speed))
    go.set_right_speed(speed - correctionNeeded(speed))

def defaultCorrection(speed):
    print "Correcting!"
    go.set_left_speed(speed - correctionNeeded(speed))
    go.set_right_speed(speed + correctionNeeded(speed))

def correctMotors(left_encoder_differential, right_encoder_differential, speed):
    if left_encoder_differential < right_encoder_differential:
        correctRight(speed)
    elif left_encoder_differential > right_encoder_differential:
        correctLeft(speed)
    else:
        defaultCorrection(speed)

def rs(INIT_LEFT, INIT_RIGHT):
    global encoder_left_init, encoder_right_init 
    encoder_left_init = INIT_LEFT
    encoder_right_init = INIT_RIGHT
    
    current_left_encoder_differential,current_right_encoder_differential = read_encoders()
    print "Current Left Encoder Value: ", current_left_encoder_differential
    print "Current Right Encoder Value: ", current_right_encoder_differential    
    correctMotors(current_left_encoder_differential, current_right_encoder_differential, go.read_motor_speed()[1])
