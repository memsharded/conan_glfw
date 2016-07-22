project(glfw_test)
cmake_minimum_required(VERSION 2.8.12)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()

if(NOT MSVC)
  ADD_DEFINITIONS ( -std=c++11 )
endif()

add_executable(glfw_test main.cpp glad.c)
target_link_libraries(glfw_test ${CONAN_LIBS})
