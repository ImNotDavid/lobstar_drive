import sys
import tty
import termios
import select

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8


class TwoKeyPublisher(Node):
    def __init__(self):
        super().__init__('two_key_publisher')
        self.publisher_ = self.create_publisher(Int8, '/direction', 10)

    def get_key_nonblocking(self):
        dr, _, _ = select.select([sys.stdin], [], [], 0.1)
        if dr:
            return sys.stdin.read(1)
        return None

    def publish_command(self, actuator, direction):
        msg = Int8()
        msg.data = (3*actuator) + direction + 1 # stop back forward, stop back forward
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: Actuator {actuator} move in direction {direction}')

    def run(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

        print("q a z (actuator 0), o k m (actuator 1)")

        try:
            while rclpy.ok():
                key = self.get_key_nonblocking()

                if key == 'q':
                    self.publish_command(0, 1)
                elif key == 'a':
                    self.publish_command(0, -1)
                elif key == 'z':
                    self.publish_command(0, 0)
                elif key == 'o':
                    self.publish_command(1, 1)
                elif key == 'k':
                    self.publish_command(1, -1)
                elif key == 'm':
                    self.publish_command(1, 0)
                else:
                    # no key pressed
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main(args=None):
    rclpy.init(args=args)
    node = TwoKeyPublisher()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()