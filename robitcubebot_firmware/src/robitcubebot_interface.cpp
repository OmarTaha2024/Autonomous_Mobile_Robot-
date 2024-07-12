#include "robitcubebot_firmware/robitcubebot_interface.hpp"
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include <pluginlib/class_list_macros.hpp>



namespace robitcubebot_firmware
{
robitcubebotInterface::robitcubebotInterface()
{
}


robitcubebotInterface::~robitcubebotInterface()
{
  if (arduino_.IsOpen())
  {
    try
    {
      arduino_.Close();
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("robitcubebotInterface"),
                          "Something went wrong while closing connection with port " << port_);
    }
  }
}


CallbackReturn robitcubebotInterface::on_init(const hardware_interface::HardwareInfo &hardware_info)
{
  CallbackReturn result = hardware_interface::SystemInterface::on_init(hardware_info);
  if (result != CallbackReturn::SUCCESS)
  {
    return result;
  }

  try
  {
    port_ = info_.hardware_parameters.at("port");
  }
  catch (const std::out_of_range &e)
  {
    RCLCPP_FATAL(rclcpp::get_logger("robitcubebotInterface"), "No Serial Port provided! Aborting");
    return CallbackReturn::FAILURE;
  }

  velocity_commands_.reserve(info_.joints.size());
  position_states_.reserve(info_.joints.size());
  velocity_states_.reserve(info_.joints.size());

  return CallbackReturn::SUCCESS;
}


std::vector<hardware_interface::StateInterface> robitcubebotInterface::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  // Provide only a position Interafce
  for (size_t i = 0; i < info_.joints.size(); i++)
  {
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &position_states_[i]));
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &velocity_states_[i]));
  }

  return state_interfaces;
}


std::vector<hardware_interface::CommandInterface> robitcubebotInterface::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  // Provide only a velocity Interafce
  for (size_t i = 0; i < info_.joints.size(); i++)
  {
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
        info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &velocity_commands_[i]));
  }

  return command_interfaces;
}


CallbackReturn robitcubebotInterface::on_activate(const rclcpp_lifecycle::State &)
{
  RCLCPP_INFO(rclcpp::get_logger("robitcubebotInterface"), "Starting robot hardware ...");

  // Reset commands and states
  velocity_commands_ = { 0.0, 0.0 };
  position_states_ = { 0.0, 0.0 };
  velocity_states_ = { 0.0, 0.0 };

  try
  {
    arduino_.Open(port_);
    arduino_.SetBaudRate(LibSerial::BaudRate::BAUD_115200);
  }
  catch (...)
  {
    RCLCPP_FATAL_STREAM(rclcpp::get_logger("robitcubebotInterface"),
                        "Something went wrong while interacting with port " << port_);
    return CallbackReturn::FAILURE;
  }

  RCLCPP_INFO(rclcpp::get_logger("robitcubebotInterface"),
              "Hardware started, ready to take commands");
  return CallbackReturn::SUCCESS;
}


CallbackReturn robitcubebotInterface::on_deactivate(const rclcpp_lifecycle::State &)
{
  RCLCPP_INFO(rclcpp::get_logger("robitcubebotInterface"), "Stopping robot hardware ...");

  if (arduino_.IsOpen())
  {
    try
    {
      arduino_.Close();
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("robitcubebotInterface"),
                          "Something went wrong while closing connection with port " << port_);
    }
  }

  RCLCPP_INFO(rclcpp::get_logger("robitcubebotInterface"), "Hardware stopped");
  return CallbackReturn::SUCCESS;
}


hardware_interface::return_type robitcubebotInterface::read(const rclcpp::Time &,
                                                          const rclcpp::Duration &)
{
    // Interpret the string
    if(arduino_.IsDataAvailable())
    {
        std::string message;
        arduino_.ReadLine(message);
        std::stringstream ss(message);
        std::string res;
        int multiplier = 1;
        while(std::getline(ss, res, ','))
        {
            multiplier = res.at(1) == 'p' ? 1 : -1;

            if(res.at(0) == 'r')
            {
                // Assuming the encoder counts or ticks are received here
                int right_encoder_counts = std::stoi(res.substr(2, res.size()));
                // Convert encoder counts to joint position (implement your conversion logic here)
                double right_joint_position = convertEncoderCountsToJointPosition(right_encoder_counts);
                // Update the position state for the right wheel joint
                position_states_.at(0) = right_joint_position;
            }
            else if(res.at(0) == 'l')
            {
                // Assuming the encoder counts or ticks are received here
                int left_encoder_counts = std::stoi(res.substr(2, res.size()));
                // Convert encoder counts to joint position (implement your conversion logic here)
                double left_joint_position = convertEncoderCountsToJointPosition(left_encoder_counts);
                // Update the position state for the left wheel joint
                position_states_.at(1) = left_joint_position;
            }
        }
      
    }
    return hardware_interface::return_type::OK;
}

// Helper function to convert encoder counts to joint position (implement your conversion logic here)
// Helper function to convert encoder counts to joint position
double robitcubebotInterface::convertEncoderCountsToJointPosition(int encoder_counts)
{
    // Assuming you have information about your encoder resolution and wheel circumference
    double encoder_resolution = 1000; // Example: 1000 counts per revolution
    double wheel_circumference = 0.2; // Example: 0.2 meters (20 cm)

    // Compute the number of revolutions based on the encoder counts
    double revolutions = encoder_counts / encoder_resolution;

    // Compute the distance traveled by the wheel
    double distance_traveled = revolutions * wheel_circumference;

    // Assuming a simple differential drive system with one encoder per wheel
    // The joint position can be represented as the distance traveled by the wheel
    return distance_traveled;
}


hardware_interface::return_type robitcubebotInterface::write(const rclcpp::Time &,
                                                          const rclcpp::Duration &)
{
  // Implement communication protocol with the Arduino
  std::stringstream message_stream;
  char right_wheel_sign = velocity_commands_.at(0) >= 0 ? 'p' : 'n';
  char left_wheel_sign = velocity_commands_.at(1) >= 0 ? 'p' : 'n';
  std::string compensate_zeros_right = "";
  std::string compensate_zeros_left = "";
  if(std::abs(velocity_commands_.at(0)) < 10.0)
  {
    compensate_zeros_right = "0";
  }
  else
  {
    compensate_zeros_right = "";
  }
  if(std::abs(velocity_commands_.at(1)) < 10.0)
  {
    compensate_zeros_left = "0";
  }
  else
  {
    compensate_zeros_left = "";
  }
  
  message_stream << std::fixed << std::setprecision(2) << 
    "r" << right_wheel_sign << compensate_zeros_right << std::abs(velocity_commands_.at(0)) << 
    ",l" <<  left_wheel_sign << compensate_zeros_left << std::abs(velocity_commands_.at(1)) << ",";

  try
  {
    arduino_.Write(message_stream.str());
  }
  catch (...)
  {
    RCLCPP_ERROR_STREAM(rclcpp::get_logger("robitcubebotInterface"),
                        "Something went wrong while sending the message "
                            << message_stream.str() << " to the port " << port_);
    return hardware_interface::return_type::ERROR;
  }

  return hardware_interface::return_type::OK;
}
}  // namespace robitcubebot_firmware

PLUGINLIB_EXPORT_CLASS(robitcubebot_firmware::robitcubebotInterface, hardware_interface::SystemInterface)