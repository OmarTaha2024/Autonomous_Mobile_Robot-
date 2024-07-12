cmake_minimum_required(VERSION 3.5)
project(robitcubebot_controller)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2 REQUIRED)
find_package(Eigen3 REQUIRED)






include_directories(include)
include_directories(${EIGEN3_INCLUDE_DIR})

add_executable(simple_controller src/simple_controller.cpp)
ament_target_dependencies(simple_controller rclcpp geometry_msgs std_msgs sensor_msgs nav_msgs tf2_ros tf2 ${Eigen_LIBRARIES})

add_executable(noisy_controller src/noisy_controller.cpp)
ament_target_dependencies(noisy_controller rclcpp geometry_msgs sensor_msgs nav_msgs tf2_ros tf2)

add_executable(teleop_publisher src/twist_publisher.cpp)
ament_target_dependencies(teleop_publisher rclcpp geometry_msgs std_msgs)

add_executable(lifter_controller src/lifter_controller.cpp)
ament_target_dependencies(lifter_controller rclcpp std_msgs)

ament_python_install_package(${PROJECT_NAME})

install(
  DIRECTORY include
  DESTINATION include
)

install(TARGETS
  simple_controller
  noisy_controller
  teleop_publisher
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch config 
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  ${PROJECT_NAME}/simple_controller.py
  ${PROJECT_NAME}/noisy_controller.py
  ${PROJECT_NAME}/twist_publisher.py
  ${PROJECT_NAME}/lifter_controller.py
  DESTINATION lib/${PROJECT_NAME}
)
ament_package()
