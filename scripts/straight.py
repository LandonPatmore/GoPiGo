import gopigo as go

# Sets the speed of the motors.
#     speed1: speed of motor1
#     speed2: speed of motor2
def set_motors(speed1, speed2):
	go.motor1(1, speed1)
	go.motor2(1, speed2)

# Get program parameters
target_speed = input("Enter target speed")
stop_dist = input("Enter target stop distance")

print "Starting rover"

# Make rover start moving
set_motors(target_speed, target_speed)

stopped = False

while True:
	dist = us_dist(15)
	
	# If stopped but no object is too close, resume
	# Else if moving and an object is too close, stop
    if stopped and dist > stop_dist:
        set_motors(target_speed, target_speed)
		stopped = False
    elif not stopped and dist < stop_dist:
        stop()
        stopped = True
	
	# If one motor is moving slower, change the other to match it
	speeds = go.read_motor_speed()
	if speeds[0] < speeds[1]:
		set_motors(target_speed, speeds[0])
	elif speeds[1] < speeds[0]:
		set_motors(speeds[1], target_speed)
	
	print "Motor1 speed = ", speeds[0], " | ",
			"Motor2 speed = ", speeds[1], " | ",
			"Sonar = ", dist