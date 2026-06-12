#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class ScaledTeleop(Node):
    def __init__(self):
        super().__init__('scaled_teleop')

        self.axis_linear_x   = 1    # left stick vertical
        self.axis_angular_yaw = 0   # left stick horizontal
        self.throttle_axis   = 2    # scale axis
        self.enable_btn      = 0    # hold to move

        self.max_linear      = 1.5  # m/s
        self.max_angular     = 8.0  # rad/s

        # axis 2 is a trigger: -1.0 (released) → 1.0 (fully pressed)
        # remapped to 0.0–1.0 scalar
        self.trigger_min = -1.0
        self.trigger_max =  1.0

        self.sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def remap(self, val, in_min, in_max, out_min, out_max):
        return (val - in_min) / (in_max - in_min) * (out_max - out_min) + out_min

    def joy_cb(self, msg: Joy):
        twist = Twist()

        if msg.buttons[self.enable_btn]:
            scalar = self.remap(
                msg.axes[self.throttle_axis],
                self.trigger_min, self.trigger_max,
                0.0, 1.0
            )

            twist.linear.x  = msg.axes[self.axis_linear_x]    * self.max_linear  * scalar
            twist.angular.z = msg.axes[self.axis_angular_yaw] * self.max_angular * scalar

        self.pub.publish(twist)

def main():
    rclpy.init()
    rclpy.spin(ScaledTeleop())

if __name__ == '__main__':
    main()