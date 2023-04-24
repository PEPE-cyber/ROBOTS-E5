import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from math import cos, sin

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

def setpoint_callback(msg):
    global setpoint
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
controller_vel = PIDController(0.1, 0.1, 0.1, dt)
controller_theta = PIDController(0.1, 0.1, 0.1, dt)

rospy.Subscriber('/pub_wl', Float32, wl_callback)
rospy.Subscriber('/pub_wr', Float32, wr_callback)

rospy.init_node('pid_controller')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
twist = Twist()



angle = 0
x = 0
y = 0
if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            # Get current velocities of each wheel
            v_l = wl
            v_r = wr
            # Get current position of the robot from each wheel velocity
            angle += r * (v_r - v_l) * dt / L
            x += r * (v_r + v_l) / 2 * dt * cos(angle)
            y += r * (v_r + v_l) / 2 * sin(angle)
            
            # Calculate the error between the current position and the setpoint
            error = Point()
            error.x = setpoint.x - x
            error.y = setpoint.y - y
            error.z = setpoint.z - angle

            #  Obtain the distance to the setpoint
            distance = (error.x**2 + error.y**2)**0.5
            controller_vel.update(distance)
            controller_theta.update(error.z)

            # Calculate the linear and angular velocity
            v = controller_vel.get_control()
            w = controller_theta.get_control()

            # Publish the linear and angular velocity
            twist.linear.x = v
            twist.angular.z = w
            pub.publish(twist)
            rospy.sleep(dt)
          
    except rospy.ROSInterruptException:
        pass