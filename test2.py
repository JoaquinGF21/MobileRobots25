from robot_systems.robot import HamBot

import math
import time
base_speed = 30
target = 250

kp = 0.06
ki = 0.001
kd = 0.03
Chris_R = HamBot()
camera = Chris_R.camera

def PID(target, current,prev_error,integral,dt):
    err = target - current
    if abs(err) > 5:
        #Proportional
        p_term = kp * err
        
        #integral
        integral += err * dt
        i_term = ki * integral
        #derivative
        derivative = (err -prev_error)/dt
        d_term = kd * derivative
        
        adj = p_term + i_term + d_term
    else:
        adj = 0
    
    return adj, err, integral
def get_lidar(dir,rL,rU):
    directions= {
        "left" : 90,
        "right": 270,
        "forw" : 180,
        "back" : 0
    }
    center = directions.get(dir)
    temp = []
    sight = Chris_R.get_range_image()
    #sets initial prev to be an array
    for i in range(rL,rU):
        idx = center + i
        if sight[idx] != -1:
            temp.append(sight[idx])
        
    if temp:
        return min(temp)
    else:
        return -1
def rotate(deg):
    axel = 152
    wheel_diameter = 90
    rotations = (axel * deg) / (360 * wheel_diameter)
    Chris_R.run_left_motor_for_rotations(rotations, 20, False)
    Chris_R.run_right_motor_for_rotations(-rotations,20, False)
    
    
def motionToGoal(color):
    camera.set_landmark_colors(color,0.25)
    
    landmark = camera.find_landmarks()
    if landmark:
        landmarkx = landmark[0].x
        if landmarkx < 280:
            adjl = 2
            adjl = -2
        if landmarkx > 360:
            adjl = -2
            adjr = 2
        if 280 <= landmarkx <= 360:
            Chris_R.set_left_motor_speed(base_speed)
            Chris_R.set_right_motor_speed(base_speed)
        Chris_R.set_left_motor_speed(base_speed + adjl)
        Chris_R.set_right_motor_speed(base_speed + adjr)
    else:
        Chris_R.set_left_motor_speed(10)
        Chris_R.set_right_motor_speed(-10)
                
                
def WallFollow(target):
    adj = 0
    perror = 0.0
    integral = 0
    ptime = time.time()
    
    while True:
        ctime = time.time()
        Chris_R.set_left_motor_speed(max(-50,min(50,base_speed + adj)))
        Chris_R.set_right_motor_speed(max(-50,min(50,base_speed - adj)))
        
        left_s = get_lidar("left",-2,20)
        forw_s = get_lidar("forw",-10,15)
        
        dt = ctime - ptime
        ptime = ctime
        if forw_s < 500:
            forw_s = get_lidar("forw",-30,15)
            forw_w = (500 - forw_s)/500
            eff_s = left_s - (forw_w*600)
        else:
            eff_s = left_s
        
        adj,perror,integral = PID(target,eff_s,perror,integral,dt)
        print(adj)
        time.sleep(0.05)
def main():
    Chris_R.stop_motors()
    time.sleep(1)
    color = (158,0,255)
    while(True):
        motionToGoal(color)
main()