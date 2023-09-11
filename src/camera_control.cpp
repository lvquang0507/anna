#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include <chrono>

using namespace std::chrono_literals;

class CameraControl : public rclcpp::Node
{
public:
    CameraControl() : Node("camera_control_node")
    {
        this->declare_parameter("position", -0.7);
        pub_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(TOPIC_NAME, 10);
        timer_ = this->create_wall_timer(500ms, std::bind(&CameraControl::timer_callback, this));
    }

private:
    void timer_callback()
    {
        double position = this->get_parameter("position").as_double();
        std_msgs::msg::Float64MultiArray msg;
        msg.data.push_back(position);

        pub_->publish(msg);
    };

    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    const std::string TOPIC_NAME = "/camera_controller/commands";
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CameraControl>());
    rclcpp::shutdown();
    return 0;
}