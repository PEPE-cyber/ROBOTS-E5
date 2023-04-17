#!/usr/bin/env python
 
import rospy
from geometry_msgs.msg import Twist
 
def move(distance, speed, cmd_vel):
    cmd_vel.linear.x = speed
    t0 = rospy.Time.now()
    distance_moved = 0
   
    while distance_moved < 2*0.90:
        pub.publish(cmd_vel)
        t1 = rospy.Time.now()
        distance_moved = speed * (t1 - t0).to_sec()
        rospy.sleep(0.01)
 
    cmd_vel.linear.x = 0
    pub.publish(cmd_vel)
 
    rospy.sleep(3)
 
def turn(angle, angular_speed, cmd_vel):
    # Girar a la izquierda
    cmd_vel.angular.z = angular_speed * 2 / 0.5
    t0 = rospy.Time.now()
    angle_turned = 0
    while angle_turned < angle*0.92:
        pub.publish(cmd_vel)
        t1 = rospy.Time.now()
        angle_turned = angular_speed * 2 / 0.5 * (t1 - t0).to_sec()
        rospy.sleep(0.01)
 
    cmd_vel.angular.z = 0
    pub.publish(cmd_vel)
 
    rospy.sleep(3)
 
# Inicializar el nodo
rospy.init_node('path_generator')
# Crear un publicador para enviar mensajes Twist
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
 
# Crear un objeto Twist para enviar los comandos
cmd_vel = Twist()
 
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0
 
pub.publish(cmd_vel)
 

if _name_ == '_main_':
    try:
        move(2, 0.3, cmd_vel)  # Avanzar
        turn(1.5708, 0.3, cmd_vel) # Girar
 
    except rospy.ROSInterruptException:
        pass