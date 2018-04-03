import gopigo as go

STOP_DISTANCE = input('Enter stop distance: ')
DISTANCE_TO_SLOW = input('Enter distance to slow down: ')
SPEED = input('Enter start speed: ')


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
    elif (distanceToObstacle() > DISTANCE_TO_SLOW) and (getCurrentSpeed() < SPEED):
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
        slowing()
    elif state.state == 2:
        accelerating(state)
    elif state.state == 3:
        stopped()

def normal():
    go.forward()

def slowing():
    go.set_speed(getCurrentSpeed() - 20)
    go.forward()

def accelerating(state):
    if(getCurrentSpeed() < SPEED):
        go.set_speed(getCurrentSpeed() + 20)
        go.forward()
    else:
        state.state = 0

def stopped():
    go.stop()

def distanceToObstacle():
    return go.us_dist(15)

def getCurrentSpeed():
    print('Current Speed: ', go.read_motor_speed()[0])
    return go.read_motor_speed()[0]

def main():
    go.set_speed(SPEED)  
    
    state = STATE()

    while True:
        stateCheck(state)

if __name__ == "__main__":
    main()
