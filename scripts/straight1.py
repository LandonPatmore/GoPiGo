import gopigo as go
import time

def set_motors(s1, s2):
    go.motor1(1, s1)
    go.motor2(1, s2)

go.trim_write(0)
lwt = go.enc_read(0)
rwt = go.enc_read(1)
oldlwt = lwt
oldrwt = rwt
target_speed = input("Speed?")
lms = target_speed
rms = target_speed
print "Starting"

set_motors(target_speed, target_speed)

while True:
    oldlwt = lwt
    oldrwt = rwt
    lwt = go.enc_read(0)
    rwt = go.enc_read(1)
    lwtdiff = lwt - oldlwt
    rwtdiff = rwt - oldrwt
    error = rwtdiff - lwtdiff
    print "L, R, E: ", lwtdiff, rwtdiff, error

#    if (error !=  0):
#        lms += error
#        go.motor1(1, lms)

    time.sleep(1)



