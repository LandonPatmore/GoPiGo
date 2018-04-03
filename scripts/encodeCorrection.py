import gopigo as go
import time
import math


# 0 - Right motor
# 1 - Left motor

# 0 - Left encoder
# 1 - Right encoder

go.set_speed(150)
go.forward()

prevLeft = go.enc_read(0)
prevRight = go.enc_read(1)

def set_slave(speed):
    go.set_right_speed(speed)

while True:
    time.sleep(0.25)
    left = go.enc_read(0)
    right = go.enc_read(1)

    leftDiff = left - prevLeft
    rightDiff = right - prevRight

    print 'TICKS LEFT:      ', leftDiff, 'TICKS RIGHT:      ', rightDiff

    error = leftDiff - rightDiff

    print 'ERROR:   ', error

    speeds = go.read_motor_speed()

    set_slave(speeds[0] + error)

    new_speeds = go.read_motor_speed()

    print 'LEFT MOTOR:      ', new_speeds[1], 'RIGHT MOTOR:      ', new_speeds[0]
    
    prevRight = right
    prevLeft = left
