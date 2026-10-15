cmake_minimum_required(VERSION 3.8)
project(das_mr_r2c)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY urdf config launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
