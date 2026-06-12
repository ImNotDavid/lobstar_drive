import sys
import tty
import termios
import select

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TwoKeyPublisher(Node):
    def __init__(self):
        super().__init__('two_key_publisher')
        self.publisher_ = self.create_publisher(String, '/direction', 10)

    def get_key_nonblocking(self):
        dr, _, _ = select.select([sys.stdin], [], [], 0.1)
        if dr:
            return sys.stdin.read(1)
        return None

    def publish_command(self, value):
        msg = String()
        msg.data = value
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: {value}')

    def run(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

        print("w for actuator0:0, s for ping2, a for actuator_0:1, d for loadcell_feedback:1")

        try:
            while rclpy.ok():
                key = self.get_key_nonblocking()

                if key == 'w':
                    self.publish_command("forward")
                elif key == 's':
                    self.publish_command("back")
                elif key == 'a':
                    self.publish_command("left")
                elif key == 'd':
                    self.publish_command("right")
                elif key == 'e':
                    self.publish_command("empty")
                elif key == 'q':
                    print("\nExiting...")
                    break
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