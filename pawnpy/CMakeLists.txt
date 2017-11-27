cmake_minimum_required(VERSION 3.1)

project(pawnpy)

#set(Boost_USE_STATIC_LIBS        ON) # only find static libs
#set(Boost_USE_MULTITHREADED      ON)
#set(Boost_USE_STATIC_RUNTIME    OFF)

if(APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
    set(CMAKE_SHARED_LIBRARY_PREFIX "")
endif(APPLE)

find_package(Boost 1.58.0 COMPONENTS system python3)
find_package(PythonLibs)

include_directories(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})

add_library(${PROJECT_NAME} SHARED "src/main.cpp")

target_link_libraries(${PROJECT_NAME} ${PYTHON_LIBRARIES} ${Boost_LIBRARIES})
