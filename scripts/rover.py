import gopigo as go
import sys

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
class STATE:
    def __init__(self):
        self.state = 0

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
    print('Current Speed: ', go.read_motor_speed()[0])
    return go.read_motor_speed()[0]

'''
Sets the motor speeds to match each other if they are different
'''
def setMotorSpeeds():
    speeds = go.read_motor_speed()

    # If one motor is moving slower, change the other to match it
    if speeds[0] < speeds[1]:
        print 'MOTOR: Left motor moving slower'
        go.set_speed(speeds[0])
    elif speeds[1] < speeds[0]:
        print 'MOTOR: Right motor moving slower'
        go.set_speed(speeds[1])

def main():
    go.trim_write(-5)

    # Sets the intitial speed to 0
    go.set_speed(0)

    # Sets the initial state to 0 = NORMAL
    state = STATE()

    # Program loop
    while True:
        try:
            stateCheck(state)

        # Shuts the ACC down when a Ctrl + c command is issued
        except KeyboardInterrupt:
            print '\nACC shut off'
            go.stop()
            sys.exit()

if __name__ == "__main__":
    main()
