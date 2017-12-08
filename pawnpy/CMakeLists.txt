cmake_minimum_required(VERSION 3.1)

project(pawnpy)

set(PAWN ${CMAKE_CURRENT_SOURCE_DIR}/src/pawn)

include(cmake.base.txt)

add_library(${PROJECT_NAME} SHARED
  ${PAWNCC_SRCS}
  ${PAWNAMX_SRCS}
)

