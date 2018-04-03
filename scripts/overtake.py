import gopigo as go
import time

go.set_speed(100)
#go.trim_write(-5)
while True:

    DISTANCE_TO_OBJECT = go.us_dist(15)
    go.forward()

    if(DISTANCE_TO_OBJECT <= 20):
#go.trim_write(-5)
        #go.forward()
        #time.sleep(3)
        go.left()
        time.sleep(1)
        #go.set_speed(200)
        go.forward()
        time.sleep(1)
        go.right()
        time.sleep(1)
        #go.set_speed(200)
        go.forward()
        #time.sleep(2)
        #go.right()
        #time.sleep(1)
        #go.forward()
        #time.sleep(1)
        #go.left()
        #time.sleep(1)
        #go.forward()
