import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from alan_interfaces.srv import RectangleArea


class RectangleAreaServer(Node):
    """Dikdörtgen alanı hesaplayan ROS 2 servis sunucusu."""

    def __init__(self) -> None:
        super().__init__('rectangle_area_server')
        self.srv = self.create_service(
            RectangleArea,
            'rectangle_area',
            self.handle_rectangle_area,
        )
        self.get_logger().info('RectangleArea servisi hazır: /rectangle_area')

    def handle_rectangle_area(
        self,
        request: RectangleArea.Request,
        response: RectangleArea.Response,
    ) -> RectangleArea.Response:
        if request.width < 0.0 or request.height < 0.0:
            response.area = 0.0
            response.success = False
            self.get_logger().warning(
                f'Negatif değer reddedildi: width={request.width}, height={request.height}'
            )
            return response

        response.area = float(request.width * request.height)
        response.success = True
        self.get_logger().info(
            f'İstek: width={request.width}, height={request.height} '
            f'-> area={response.area}, success={response.success}'
        )
        return response


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RectangleAreaServer()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
