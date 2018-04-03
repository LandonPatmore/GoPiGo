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

def normal():
    go.forward()

def slowing(state):
    if(getCurrentSpeed() >= MIN_SPEED):
        go.set_speed(getCurrentSpeed() - 10)
        go.forward()
    else:
        state.state = 0

def accelerating(state):
    if(getCurrentSpeed() < MAX_SPEED):
        go.set_speed(getCurrentSpeed() + 10)
        go.forward()
    else:
        state.state = 0

def stopped():
    go.set_speed(0)
    go.stop()

def distanceToObstacle():
    return go.us_dist(15)

def getCurrentSpeed():
    print('Current Speed: ', go.read_motor_speed()[0])
    return go.read_motor_speed()[0]

def main():
    go.set_speed(0)  
    
    state = STATE()

    while True:
        try:
            stateCheck(state)
        except KeyboardInterrupt:
            print '\nACC shut off'
            go.stop() 
            sys.exit()

if __name__ == "__main__":
    main()
