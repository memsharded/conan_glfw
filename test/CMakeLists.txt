project(glfw_test)
cmake_minimum_required(VERSION 2.8.12)

include_directories(${glfw_test_SOURCE_DIR})
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()

ADD_DEFINITIONS ( -std=c++11 )

add_executable(glfw_test main.cpp glad.c)
target_link_libraries(glfw_test ${CONAN_LIBS})
