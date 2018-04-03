import gopigo as go

targetSpeed = input("Enter target speed: ")
stop_dist = input("Enter target stop distance: ")

speed = 90

go.set_speed(speed)

max_speed = 150

go.forward()

stopped = False

while True:
	dist = go.us_dist(25) 
	if speed < targetSpeed: 
 		go.increase_speed()
	if (speed == max_speed):
		go.set_speed(max_speed)	
	elif dist < stop_dist:
		go.stop()
		stopped = True
	print "Speed = ", speed, "|", "Sonar = ", dist 

