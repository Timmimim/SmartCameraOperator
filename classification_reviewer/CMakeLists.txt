cmake_minimum_required(VERSION 3.10)
project(classification_reviewer)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_C_COMPILER /usr/bin/gcc-8)
set(CMAKE_CXX_COMPILER /usr/bin/g++-8)

find_package(OpenCV REQUIRED )

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

set(CMAKE_CXX_FLAGS "-lstdc++fs")

add_executable(classification_reviewer
        src/main.cpp)

target_link_libraries( classification_reviewer ${OpenCV_LIBS} stdc++fs)