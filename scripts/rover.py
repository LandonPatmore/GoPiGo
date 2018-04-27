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

'''
Motors:
0 - Right
1 - Left

Encoders:
0 - Left 
1 - Right
'''

'''
Class to determine the state of the rover
'''
class STATE(object):
    def __init__(self):
        self.state = 0

'''
Class to keep data on encoders
'''
class Encoders(object):
    def __init__(self, startLeft, startRight):
        self.oldLeft = startLeft
        self.oldRight = startRight
        self.currentLeft = 0
        self.currentRight = 0

    '''
    Calculates the difference between the current ticks and the previous ticks
    '''
    def getDiffs(self):
        leftDiff = self.currentLeft - self.oldLeft
        rightDiff = self.currentRight - self.oldRight

        # print 'Left diff: ', leftDiff
        # print 'Right diff: ', rightDiff

        return (leftDiff, rightDiff)
    
    '''
    Determines the error between the left and right encoders

    Parameters
    ----------
    left: Int
        Left encoder value
    right: Int
        Right encoder value
    '''
    def getError(self, left, right):
        return left - right
    
    '''
    Updates the current values of the encoders
    left: Int
        Current left encoder value
    right: Int
        Current right encoder value
    '''
    def updateCurrentValues(self, left, right):
        if((left - self.currentLeft) > -1):
            self.currentLeft = left
        if((right - self.currentRight) > - 1):
            self.currentRight = right

    '''
    Replaces the old values with the current values
    '''
    def replaceOldValues(self):
        self.oldLeft = self.currentLeft
        self.oldRight = self.currentRight

    '''
    Custom toString metho
    '''
    def __str__(self):
        return 'oldLeft:    ' + str(self.oldLeft) + ' currentLeft:    ' + str(self.currentLeft) + '\noldRight:     ' + str(self.oldRight) + ' currentRight:    ' + str(self.currentRight)

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
        go.set_speed(getCurrentSpeed() - 1)
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
        go.set_speed(getCurrentSpeed() + 1)
        go.forward()
    else:
        state.state = 0

'''
Stops the rover and sets the speed of the motors to be 0
'''
def stopped():
    go.stop()

'''
Gets the distance to the obstacle in front of the rover
'''
def distanceToObstacle():
    return go.us_dist(15)

'''
Gets the current speed of the rover from the motor
'''
def getCurrentSpeed():
    return go.read_motor_speed()[1]

'''
Adds the error to the slave motor (right) so it either speeds up or slows down to match the master motor (left)

Parameters
----------
error: Int
    The error (difference) between the left and right encoders
'''
def set_slave_motor(error):
    go.set_right_speed(go.read_motor_speed()[0] + error)

'''
Gets the values of the left and right encoders
'''
def read_encoders():
    return (go.enc_read(0), go.enc_read(1))

'''
Calulates the error between the left and right encoders

Parameters
----------
encoders: Tuple
    Left and right encoder values
'''
def calculateEncodersError(encoders):    
    encoders.updateCurrentValues(*read_encoders())
    print encoders
    diffs = encoders.getDiffs()
    error = encoders.getError(*diffs)
    
    print 'Error:   ', error

    set_slave_motor(error)

    encoders.replaceOldValues()

def main():
    # Sets the intitial speed to 0
    go.set_speed(50)
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
