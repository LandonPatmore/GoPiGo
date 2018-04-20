# Adapted from: Basic Obstacle Avoid
# URL: https://github.com/DexterInd/GoPiGo/blob/master/Software/Python/Examples/Ultrasonic_Basic_Obstacle_Avoider/basic_obstacle_avoid.py 

from gopigo import *
import time

distance_to_stop = 45
print "Press Enter to start"
raw_input()
fwd()

trim_write(1)

stopped = False

while True:
    dist=us_dist(15)
    if stopped and dist > distance_to_stop:
        fwd()
    print 'Dist: ', dist, 'cm'
    if dist < distance_to_stop:
        print "Stopping"
        right()
        stopped = True
