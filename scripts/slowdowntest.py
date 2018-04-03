import gopigo as go

critical_distance = input("Enter Critical Stop Distance: ")
slowdown_distance = input("Enter Distance where Slowdown begins: ")
initial_speed = input("Input starting speed: ")
target_speed = input("Input target speed: ")

temp_speed = initial_speed

go.set_speed(initial_speed)
go.forward()


while True:
    
    us_Distance = go.us_dist(15)


    
    if (us_Distance <= critical_distance):
    	go.stop()
    elif ((us_Distance <= slowdown_distance)): 
        if(target_speed < initial_speed):
	    while(temp_speed > target_speed):
                us_Distance = go.us_dist(15)
               # print "Distance to object: ", us_Distance, " Critical Distance: ", critical_distance
                if (us_Distance <= critical_distance):
                #    print "INSIDE: Distance to object: ", us_Distance, " Critical Distance: ", critical_distance
    	            break
        	temp_speed = temp_speed - 2
                #print "Current TempSpeed: ", temp_speed, "Current TargetSpeed: ", target_speed
    		go.set_speed(temp_speed)
  
                print "Currentspeed is: ", go.read_motor_speed()
                    


    
                            
					
			







