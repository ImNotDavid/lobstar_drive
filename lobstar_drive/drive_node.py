import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial


class DriveNode(Node):
    def __init__(self):
        super().__init__('drive_node')

        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)
        # Distance between left and right wheels in metres
        self.declare_parameter('wheel_separation', 0.250)
        # Clamp individual motor commands to this value (mm/s)
        self.declare_parameter('max_speed', 1500)

        port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud = self.get_parameter('baud_rate').get_parameter_value().integer_value

        self.wheel_separation = (
            self.get_parameter('wheel_separation').get_parameter_value().double_value
        )
        self.max_speed = (
            self.get_parameter('max_speed').get_parameter_value().integer_value
        )

        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
        self.get_logger().info(f'Opened serial port {port} at {baud} baud')

        self.create_subscription(Twist, 'cmd_vel', self._cmd_vel_cb, 10)

    def _cmd_vel_cb(self, msg: Twist):
        half_sep = self.wheel_separation / 2.0
        v_left = msg.linear.x - msg.angular.z * half_sep   # m/s
        v_right = msg.linear.x + msg.angular.z * half_sep  # m/s

        # Convert to mm/s and apply forward-direction sign convention [-,+,+,-]
        # Left side  (M1, M4): negative = forward
        # Right side (M2, M3): positive = forward
        m1 = int(-v_left * 1000)
        m2 = int(v_right * 1000)
        m3 = int(v_right * 1000)
        m4 = int(-v_left * 1000)

        limit = self.max_speed
        m1 = max(-limit, min(limit, m1))
        m2 = max(-limit, min(limit, m2))
        m3 = max(-limit, min(limit, m3))
        m4 = max(-limit, min(limit, m4))

        cmd = f'$spd:{m1},{m2},{m3},{m4}#\n'
        self.ser.write(cmd.encode())

    def destroy_node(self):
        if self.ser.is_open:
            self.ser.write(b'$spd:0,0,0,0#\n')
            self.ser.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DriveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
