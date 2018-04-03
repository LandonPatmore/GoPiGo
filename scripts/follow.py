import gopigo as go

speed = input("Enter target speed")
stop_dist = input("Enter target stop distance")

trim_write(speed)
go.forward()

stopped = False

while True:
    dist = go.us_dist(15)
    if stopped and dist > stop_dist:
        go.forward()
    elif dist < stop_dist:
        go.stop()
        stopped = True
