#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from math import cos, sin, atan2, pi

# ceate a PID controller class
class PIDController:
    def __init__(self, kp, ki, kd, dt):
        # define the PID constants
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt 
        # Initialize the variables
        self.error = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0
        self.setpoint = 0

    def update(self, error):
        # Update the error
        self.error = error
        # Calculate the integral with the trapezoidal rule
        self.integral += (self.error + self.last_error) * self.dt / 2
        # Calculate the derivative
        self.derivative = (self.error - self.last_error) / self.dt
        self.last_error = self.error

    def get_control(self):
        # Obtain the control variable
        return self.kp * self.error + self.ki * self.integral + self.kd * self.derivative
    
    def update_setpoint(self, setpoint):
        # Update the setpoint
        self.setpoint = setpoint

# Define global variables and callbacks to update them
setpoint = Point()
wl = 0.0
wr = 0.0
angle_set = False
distance_set = False 
def setpoint_callback(msg):
    global setpoint, angle_set, distance_set
    print("set to", msg)
    print("changged", not setpoint == msg)
    if not setpoint == msg: 
        angle_set = False
        distance_set = False
    setpoint = msg

def wl_callback(msg):
    global wl
    wl = msg.data

def wr_callback(msg):
    global wr
    wr = msg.data


# Define constants of the model
r = 0.05
L = 0.19
dt = 0.1


# subscribe to the topic /path_generator
rospy.Subscriber('/set_point', Point, setpoint_callback)



# Create controllers for linear and angular velocity
controller_vel = PIDController(2, 0, 0, dt)
controller_theta = PIDController(4, 0, 0, dt)

rospy.Subscriber('/wl', Float32, wl_callback)
rospy.Subscriber('/wr', Float32, wr_callback)

rospy.init_node('pid_controller')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


count = 0
angle = 0 
x = 0
y = 0
if __name__ == '__main__':
    try:
        twist = Twist()
        print("init")
        twist.linear.x = 0
        twist.angular.z = 0
        for i in range(100):
            rospy.sleep(0.01)
            pub.publish(twist)
        rospy.sleep(1)
        print("start")
        while not rospy.is_shutdown():
            # Get current velocities of each wheel
            v_l = wl
            v_r = wr
            # Get current position of the robot from each wheel velocity
            angle += r * (v_r - v_l) * dt / L
            x += r * (v_r + v_l) / 2 * dt * cos(angle)
            y += r * (v_r + v_l) / 2 * dt * sin(angle)

            # Calculate the error between the current position and the setpoint
            # error = Point() 
            # error.x = setpoint.x - y
            # error.y = setpoint.y - x
            # print("error.x:", error.x, "error.y:", error.y)
            
            # Calculate the required angle to the setpoint
            angleToSetpoint = atan2(setpoint.y - y, setpoint.x - x)
            angle_error = ( angleToSetpoint - angle) % (2 * 3.14)
            # print("angleToSetpoint:", round(angleToSetpoint, 2))
            if angle_error > 3.14:
                angle_error -= 2 * 3.14
            
            # print("setpoint x:", round(setpoint.x, 2), "setpoint y:", round(setpoint.y, 2))
           

            #  Obtain the distance to the setpoint
            distance = (((setpoint.x- x) ** 2 + (setpoint.y - y) ** 2) ** 0.5)  * ( -1 if abs(round(angle_error,2)) == 3.14 else 1)
            controller_vel.update(distance)
            controller_theta.update(angle_error)
            # print("x:", round(x, 2), "y:", round(y, 2), "angle_error:", round(angle_error,2))
            # print("dis", distance)


            if (distance < 0.05):
                distance_set = True
            # Calculate the linear and angular velocity
            v = controller_vel.get_control() 
            w = controller_theta.get_control()
            
            # Publish the linear and angular velocity
            if abs(angle_error) < 0.01:
                count += 1
                if not (count < 10):
                    angle_set = True
            else:
                count = 0



            if not angle_set:
                v = 0
            else:
                w = 0
                if  distance_set:
                    v = 0


            maxSpeed = 1
            if v > maxSpeed:
                v = maxSpeed
            elif v < -maxSpeed:
                v = -maxSpeed
            if w > maxSpeed:
                w = maxSpeed
            elif w < -maxSpeed:
                w = -maxSpeed

            twist.linear.x = v
            twist.angular.z = w
            # print("v", v, "w", w)
            pub.publish(twist)
            rospy.sleep(dt)
    

    except rospy.ROSInterruptException:
        pass