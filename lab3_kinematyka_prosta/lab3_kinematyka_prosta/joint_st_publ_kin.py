import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
from rclpy.parameter import Parameter
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.msg import ParameterDescriptor
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.msg import ParameterValue


class JointStatePublisher(Node):

    def __init__(self):

        super().__init__('joint_state_publisher')
        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, '/joint_states', qos_profile)
        timer_period = 0.1  # czas w sekundach
        self.timer = self.create_timer(timer_period, self.send_message)
        print("Sending desired joint positions...")


        my_parameter_descriptor_joint1 = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set desired position of first joint.')
        my_parameter_descriptor_joint2 = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set desired position of second joint.')
        my_parameter_descriptor_joint3 = ParameterDescriptor(type=ParameterType.PARAMETER_STRING,
                                                      description='Set desired position of third joint.')

        # Deklaracja parametrów
        self.declare_parameter('joint1_pose', 0.0 , my_parameter_descriptor_joint1)
        self.declare_parameter('joint2_pose', 0.0 , my_parameter_descriptor_joint2)
        self.declare_parameter('joint3_pose', 0.0 , my_parameter_descriptor_joint3)



    def send_message(self):

        # Pobranie wartości parametrów
        my_param_joint1 = self.get_parameter('joint1_pose').get_parameter_value()
        my_param_joint2 = self.get_parameter('joint2_pose').get_parameter_value()
        my_param_joint3 = self.get_parameter('joint3_pose').get_parameter_value()


        joint_state = JointState()


        now = self.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        joint_state.name = ['base_link__link1', 'link1__link2', 'link2__link3']


        # Tu jest problem
        # my_param_joint_1 i pozostałe to obiekty klasy ParameterValue
        # Nie bardzo chcą się konwertować, a w joint_state_message muszą być float
        
        joint_state.position = [0.33 , 1.53 , 0.2342]

        self.joint_pub.publish(joint_state)


def main(args = None):
    rclpy.init(args=args)

    joint_state_publisher = JointStatePublisher()

    rclpy.spin(joint_state_publisher)

    joint_state_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()