import sys
import tty
import termios
import select

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy    


class JoyPublisher(Node):
    def __init__(self):
        super().__init__('joy_publisher')
        self.publisher_ = self.create_publisher(Int8, '/direction', 10)
        self.sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)
        self.prev_command = [0,0]

    def publish_command(self, actuator, direction):
        msg = Int8()
        msg.data = (3*actuator) + direction + 1 # stop back forward, stop back forward
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: Actuator {actuator} move in direction {direction}')

    
    def joy_cb(self,msg: Joy):
        command = [self.prev_command[0],self.prev_command[1]]

        if msg.buttons[2]:
            command[0] = 0

        if msg.buttons[4]:
            command[0] = 1
        
        if (msg.buttons[4]==0)and(msg.buttons[2]==0):
            command[0] = -1
        
        if  msg.buttons[5]:
            command[1] = 1
        
        if msg.buttons[3]:
            command[1] = 0
        
        if (msg.buttons[5]==0)and(msg.buttons[3]==0):
            command[1] = -1
        

        if(command[0]!=self.prev_command[0]):
            self.publish_command(0,command[0])
        if(command[1]!=self.prev_command[1]):
            self.publish_command(1,command[1])
        
        self.prev_command=command.copy()

        return



def main(args=None):
    rclpy.init(args=args)
    node = JoyPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()