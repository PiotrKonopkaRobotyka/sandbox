cmake_minimum_required(VERSION 3.17)
project(RobotProject)

#StandardC++ 20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON) 

#Opcje komplilatora: (-Wall) (Włącz wszystkie ostrzeżenia)
add_compile_options(-Wall -Wextra)

#Dfiniujemy co składa się na nasz program
add_executable(robot_node
    src/main.cpp
    src/motor.cpp
)

#Mówimy kompilatorowi, gdzie szukać plików .hpp (w include)
target_include_directories(robot_node PUBLIC include)