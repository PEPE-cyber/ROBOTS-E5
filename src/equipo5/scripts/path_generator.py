#!/usr/bin/env python
 
import rospy
from geometry_msgs.msg import Twist
 
def move(pub, distance, speed, cmd_vel):
    
    cmd_vel.linear.x = speed
    distance_moved = 0
    t0 = 0
    while distance_moved < distance:
        pub.publish(cmd_vel)
        if t0 == 0:
            t0 = t1 = rospy.Time.now().to_sec()
        else:
            t1 = rospy.Time.now().to_sec()
        distance_moved = speed * 1.14 * (t1 - t0)
        rospy.sleep(0.01)
 
    cmd_vel.linear.x = 0
    pub.publish(cmd_vel)
 
    rospy.sleep(0.5)
 
def turn(angle, angular_speed, cmd_vel):
    # Girar a la izquierda
    cmd_vel.angular.z = angular_speed 
    t0 = 0
    angle_turned = 0
    while angle_turned < angle:
        pub.publish(cmd_vel)
        if t0 == 0:
            t0 = t1 = rospy.Time.now().to_sec()
        else:
            t1 = rospy.Time.now().to_sec()
        angle_turned = angular_speed  * 0.88 * (t1 - t0)
        rospy.sleep(0.01)
 
    cmd_vel.angular.z = 0
    print(angle_turned)
    pub.publish(cmd_vel)
    rospy.sleep(0.5)
 
# Inicializar el nodo
rospy.init_node('path_generator')
# Crear un publicador para enviar mensajes Twist
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
 
# Crear un objeto Twist para enviar los comandos
cmd_vel = Twist()
 
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0
 
pub.publish(cmd_vel)
rospy.sleep(2)

if __name__=='__main__':
    try:
      
        for i in range(0, 4):
            move(pub, 2, 0.3, cmd_vel)
            turn(1.5708, 3, cmd_vel)
        
        cmd_vel.linear.x = 0
        cmd_vel.angular.z = 0
        pub.publish(cmd_vel)
 
    except rospy.ROSInterruptException:
        pass