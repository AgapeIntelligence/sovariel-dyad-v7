cmake_minimum_required(VERSION 3.5)
project(dyad_node)
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(fftw3 REQUIRED)

add_executable(dyad_node src/dyad_node.cpp)
ament_target_dependencies(dyad_node rclcpp std_msgs)
target_link_libraries(dyad_node PRIVATE fftw3)

install(TARGETS dyad_node DESTINATION lib/${PROJECT_NAME})
ament_package()