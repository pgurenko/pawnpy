cmake_minimum_required(VERSION 3.1)

project(pawnpyTest)

set(PAWNPY ${CMAKE_CURRENT_SOURCE_DIR}/../../pawnpy)
set(PAWN ${PAWNPY}/src/pawn)

include(${PAWNPY}/cmake.base.txt)

set(GTEST_DIR src/gtest/googletest)

include_directories(
  ${GTEST_DIR}
  ${GTEST_DIR}/include
)

add_executable(${PROJECT_NAME}
  ${PAWNCC_SRCS}
  ${GTEST_DIR}/src/gtest-all.cc
  ${GTEST_DIR}/src/gtest_main.cc
  src/pawnpyTest.cpp)

target_link_libraries(${PROJECT_NAME} ${PYTHON_LIBRARIES} ${Boost_LIBRARIES})
