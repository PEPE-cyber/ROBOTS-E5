#!/usr/bin/env python
 
import rospy
from geometry_msgs.msg import Point
 
# Inicializar el nodo
rospy.init_node('path_generator')
# Crear un publicador para enviar mensajes Twist
pub = rospy.Publisher('/set_point', Point, queue_size=10)
 
# Crear un objeto Point
point = Point()

point.linear.x = 0
point.angular.y = 0
 
pub.publish(point)
rospy.sleep(2)

if __name__=='__main__':
    try:
        while not rospy.is_shutdown():
            point.linear.x = 2
            point.angular.y = 2
            point.linear.z = 0
            pub.publish(point)
            rospy.sleep(2)

        point.linear.x = 0
        point.angular.y = 0
        pub.publish(point)
    
    except rospy.ROSInterruptException:
        pass