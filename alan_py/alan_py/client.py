import sys

import rclpy
from rclpy.node import Node
from rclpy.utilities import remove_ros_args

from alan_interfaces.srv import RectangleArea


class RectangleAreaClient(Node):
    """Komut satırından aldığı width ve height değerlerini servise gönderen istemci."""

    def __init__(self) -> None:
        super().__init__('rectangle_area_client')
        self.cli = self.create_client(RectangleArea, 'rectangle_area')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('/rectangle_area servisi bekleniyor...')

    def send_request(self, width: float, height: float):
        request = RectangleArea.Request()
        request.width = width
        request.height = height
        return self.cli.call_async(request)


def main(args=None) -> None:
    cli_args = remove_ros_args(args if args is not None else sys.argv)[1:]
    if len(cli_args) != 2:
        print('Kullanım: ros2 run alan_py client <width> <height>', file=sys.stderr)
        sys.exit(1)

    try:
        width = float(cli_args[0])
        height = float(cli_args[1])
    except ValueError:
        print('Hata: width ve height geçerli sayı olmalıdır.', file=sys.stderr)
        sys.exit(1)

    rclpy.init(args=args)
    node = RectangleAreaClient()
    try:
        future = node.send_request(width, height)
        rclpy.spin_until_future_complete(node, future)
        response = future.result()

        if response is None:
            node.get_logger().error('Servis çağrısı başarısız oldu.')
            sys.exit(1)

        if response.success:
            node.get_logger().info(
                f'Sonuç: width={width}, height={height} -> '
                f'area={response.area} (success={response.success})'
            )
        else:
            node.get_logger().warning(
                f'İstek reddedildi: width={width}, height={height} -> '
                f'area={response.area} (success={response.success})'
            )
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
