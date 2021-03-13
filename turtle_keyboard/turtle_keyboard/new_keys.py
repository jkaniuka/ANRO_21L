#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imporuję moduły ROS2
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.parameter import Parameter

# curses to biblioteka konsolowa
import curses
stdscr = curses.initscr() # inicjalizacja
curses.cbreak() # cbreak pozwala na wczytywanie przycisków bez klikania ENTER
stdscr.keypad(1) # zapewnia poprawną obsługę znaków specjalnych

stdscr.addstr(0,10,"Use defined keys to move the turtle")
stdscr.refresh() # update ekranu w konsoli

# Moduły do obsługi parametrów
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.msg import ParameterDescriptor

class MyPublisher(Node):

    def __init__(self):
        super().__init__('my_publisher_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        timer_period = 0.1  # czas w sekundach
        self.timer = self.create_timer(timer_period, self.turtle_movement)

        # opisy parametrów (do wywołania przez ros2 param describe)
        my_parameter_descriptor_up = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set the UP KEY!')
        my_parameter_descriptor_down = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set the DOWN KEY!')
        my_parameter_descriptor_left = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set the LEFT KEY!')
        my_parameter_descriptor_right = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set the RIGHT KEY!')



        # Deklaracja parametrów
        self.declare_parameter('up', 'w', my_parameter_descriptor_up)
        self.declare_parameter('down', 's', my_parameter_descriptor_down)
        self.declare_parameter('left', 'a', my_parameter_descriptor_left)
        self.declare_parameter('right', 'd', my_parameter_descriptor_right)

    def turtle_movement(self):

        

        # Pobranie wartości parametrów
        my_param_up = self.get_parameter('up').get_parameter_value().string_value
        my_param_down = self.get_parameter('down').get_parameter_value().string_value
        my_param_left = self.get_parameter('left').get_parameter_value().string_value
        my_param_right = self.get_parameter('right').get_parameter_value().string_value


        msg = Twist()
        key = ''
        key = stdscr.getch() #obsługa klinięcia
        stdscr.refresh()
        if key == ord(my_param_up): # ord() obsługuje znaki w UNICODE, żeby działało :)
            print("Up")
            msg.linear.x = 1.0
            self.publisher_.publish(msg)
        elif key == ord(my_param_down): 
            print("Down")
            msg.linear.x = -1.0
            self.publisher_.publish(msg)
        elif key == ord(my_param_left): 
            print("Left")
            msg.angular.z = 1.0
            self.publisher_.publish(msg)
        elif key == ord(my_param_right): 
            print("Right")
            msg.angular.z = -1.0
            self.publisher_.publish(msg)


def main(args=None):
    
    rclpy.init()

    my_publisher_node = MyPublisher()

    rclpy.spin(my_publisher_node)

    my_publisher_node.destroy_node()
    rclpy.shutdown()
    curses.endwin()

if __name__ == '__main__':
    main()