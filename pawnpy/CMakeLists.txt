cmake_minimum_required(VERSION 3.1)

project(pawnpy)

set(PAWN ${CMAKE_CURRENT_SOURCE_DIR}/pawn)
set(PAWNAMX ${CMAKE_CURRENT_SOURCE_DIR}/pawn/amx)

IF(APPLE)
  add_definitions(-DHAVE_SAFESTR)
ENDIF(APPLE)

add_subdirectory(pawn)

include_directories(
  ${PAWN}/linux
)

add_library(pawnpy SHARED
  ${PAWNAMX}/amx.c
  ${PAWNAMX}/amxaux.c
)

