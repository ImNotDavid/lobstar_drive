import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String, Int8
import serial
import threading


class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud', 115200)

        port = self.get_parameter('port').value
        baud = self.get_parameter('baud').value

        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            self.get_logger().info(f'Opened serial port {port} at {baud}')
        except Exception as e:
            self.get_logger().error(f'Failed to open serial port: {e}')
            raise

        self.status_pub = self.create_publisher(String, '/esp32_status', 10)

        self.subscription = self.create_subscription(
            Int8,
            '/direction',
            self.listener_callback,
            10
        )

        self.reader_thread = threading.Thread(target=self.read_serial_loop, daemon=True)
        self.reader_thread.start()

    def listener_callback(self, msg):
        actuator = 0 if (msg.data < 3) else 1
        direction = (msg.data-(3*actuator)) - 1
        cmd = f"<ACTUATOR_{actuator}:{direction}>\n"
        self.ser.write(cmd.encode())
        self.get_logger().info(f'Sent to ESP32: {cmd.strip()}')

    def read_serial_loop(self):
        while rclpy.ok():
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode(errors='ignore').strip()
                    if line:
                        ros_msg = String()
                        ros_msg.data = line
                        self.status_pub.publish(ros_msg)
                        self.get_logger().info(f'ESP32 says: {line}')
            except Exception as e:
                self.get_logger().error(f'Serial read error: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()