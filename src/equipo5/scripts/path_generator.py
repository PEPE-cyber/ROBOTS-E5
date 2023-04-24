#!/usr/bin/env python
 
import rospy
from geometry_msgs.msg import Point
 
# Inicializar el nodo
rospy.init_node('path_generator')
# Crear un publicador para enviar mensajes Twist
pub = rospy.Publisher('/set_point', Point, queue_size=10)
 
# Crear un objeto Point
point = Point()

point.x = 0
point.y = 0
 
pub.publish(point)
rospy.sleep(2)

if __name__=='__main__':
    try:
        while not rospy.is_shutdown():
            point.x = 1.70
            point.y = 0
            pub.publish(point)
            print("point", 1)
            rospy.sleep(10)
            point.x = 1.70
            point.y = 1.70
            pub.publish(point)
            print("point", 2)
            rospy.sleep(10)
            point.x = 1.70
            point.y = 0
            pub.publish(point)
            print("point", 3)
            rospy.sleep(10)
            point.x = 0
            point.y = 0
            pub.publish(point)
            print("point", 4)
            rospy.sleep(10)

        point.linear.x = 0
        point.angular.y = 0
        pub.publish(point)
    
    except rospy.ROSInterruptException:
        pass