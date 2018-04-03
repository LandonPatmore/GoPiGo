import gopigo as go
import sys
import time

STOP_DISTANCE = input('Enter stop distance: ')
DISTANCE_TO_SLOW = input('Enter distance to slow down: ')
MIN_SPEED = input('Enter minimum speed: ')
MAX_SPEED = input('Enter max speed: ')

'''
0 - Normal
1 - Slowing Down
2 - Speeding Up
3 - Stop
'''
class STATE(object):
    def __init__(self):
        self.state = 0

# 0 - Right motor
# 1 - Left motor

# 0 - Left encoder
# 1 - Right encoder
class Encoders(object):
    def __init__(self, startLeft, startRight):
        self.oldLeft = startLeft
        self.oldRight = startRight
        self.currentLeft = 0
        self.currentRight = 0

    def getDiffs(self):
        leftDiff = self.currentLeft - self.oldLeft
        rightDiff = self.currentRight - self.oldRight

        return (leftDiff, rightDiff)

    def getError(self, left, right):
        return left - right
    
    def updateCurrentValues(self, left, right):
        self.currentLeft = left
        self.currentRight = right

    def replaceOldValues(self):
        self.oldLeft = self.currentLeft
        self.oldRight = self.currentRight

'''
Checks the distance between the rover and the obstacle ahead and changes the state based on the distance to the obstacle

Parameters
----------
state: STATE
    The current state of the rover
'''
def checkDistance(state):
    print("Current distance to obstacle: ", distanceToObstacle())
    if distanceToObstacle() <= STOP_DISTANCE:
        print('STATE: STOP')
        state.state = 3
    elif distanceToObstacle() <= DISTANCE_TO_SLOW:
        print('STATE: SLOW DOWN')
        state.state = 1
    elif (distanceToObstacle() > DISTANCE_TO_SLOW) and (getCurrentSpeed() < MAX_SPEED):
        print('STATE: SPEED UP')
        state.state = 2
    else:
        print('STATE: NORMAL')
        state.state = 0

'''
Checks the current state of the rover and runs the function based on the current state

Parameters
----------
state: STATE
    The current state of the rover
'''
def stateCheck(state):
    checkDistance(state)
    if state.state == 0:
        normal()
    elif state.state == 1:
        slowing(state)
    elif state.state == 2:
        accelerating(state)
    elif state.state == 3:
        stopped()

'''
The normal operation of the rover which just moves forward at the speed it is at, which is the max speed
'''
def normal():
    go.forward()

'''
Slows the rover down if the current speed is above the MIN_SPEED

Parameters
----------
state: STATE
    The current state of the rover
'''
def slowing(state):
    if(getCurrentSpeed() >= MIN_SPEED):
        go.set_speed(getCurrentSpeed() - 10)
        go.forward()
    else:
        state.state = 0

'''
Accelerates the rover if the current speed is less than the MAX_SPEED

Parameters
----------
state: STATE
    The current state of the rover
'''
def accelerating(state):
    if(getCurrentSpeed() < MAX_SPEED):
        go.set_speed(getCurrentSpeed() + 25)
        go.forward()
    else:
        state.state = 0

'''
Stops the rover and sets the speed of the motors to be 0
'''
def stopped():
    go.stop()
    go.set_speed(0)

'''
Gets the distance to the obstacle in front of the rover
'''
def distanceToObstacle():
    return go.us_dist(15)

'''
Gets the current speed of the rover from the motor
'''
def getCurrentSpeed():
#    print('Current Speed: ', go.read_motor_speed()[1])
    return go.read_motor_speed()[1]

def set_slave_motor(speed):
    go.set_right_speed(speed)

def read_encoders():
    return (go.enc_read(0), go.enc_read(1))

def calculateEncodersError(encoders):
#    time.sleep(0.25)

    
    encoders.updateCurrentValues(*read_encoders())
    diffs = encoders.getDiffs()
    error = encoders.getError(*diffs)
    
    print 'Error:   ', error

def main():
    # Sets the intitial speed to 0
    go.set_speed(0)
    
    # Sets the initial encoder values
    encoders = Encoders(*read_encoders())

    # Sets the initial state to 0 = NORMAL
    state = STATE()

    # Program loop
    while True:
        try:
            calculateEncodersError(encoders)
            stateCheck(state)
            
        # Shuts the ACC down when a Ctrl + c command is issued
        except KeyboardInterrupt:
            print '\nACC shut off'
            go.stop()
            sys.exit()

if __name__ == "__main__":
    main()
