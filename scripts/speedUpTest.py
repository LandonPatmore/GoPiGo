import gopigo as go

targetSpeed = input("Enter target speed: ")
stop_dist = input("Enter target stop distance: ")

speed = 90

go.set_speed(speed)

max_speed = 150

go.forward()

stopped = False

while True:
	dist = go.us_dist(15) 
	if speed < targetSpeed:
            go.increase_speed()
	elif dist < stop_dist:
		go.stop()
		stopped = True
	print "Speed = ", speed, "|", "Sonar = ", dist 

