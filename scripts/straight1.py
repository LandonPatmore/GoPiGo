import gopigo as go

def set_motors(s1, s2):
    go.motor1(1, s1)
    go.motor2(1, s2)

lwt = go.enc_read(0)
rwt = go.enc_read(1)
target_speed = input("Speed?")
print "Starting"
lws = target_speed
rws = target_speed

set_motors(target_speed, target_speed)

while True:
    lwt -= go.enc_read(0)
    rwt -= go.enc_read(1)
    error = rwt - lwt
    lws += error/2
    rws += error/2
    if error > 0:
        if rws == target_speed:
            lws += 2
            go.motor1(1, lws) 
        else:
            rws -= 2
            go.motor2(1, rws)
