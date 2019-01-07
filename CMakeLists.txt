cmake_minimum_required (VERSION 3.8.2)
project (Walkers LANGUAGES CXX VERSION 1.0.1 DESCRIPTION "Random Walkers simulator")
set (CMAKE_CXX_STANDARD 17)
set (CMAKE_CXX_STANDARD_REQUIRED ON)

# Walkers Version
set (MAJOR    1)
set (MINOR    0)
set (REVISION 0)
add_definitions (-DMAJOR=${MAJOR} -DMINOR=${MINOR} -DREVISION=${REVISION})

#################################################################
#                         COMPILE OPTIONS                       #
#################################################################

option (OMP     "Enable OpenMP                support" ON  )

#################################################################
#                         SETTING VARIABLES                     #
#################################################################

set (CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake/Modules/" ${CMAKE_MODULE_PATH})

if ( NOT APPLE )
  set (CMAKE_SKIP_BUILD_RPATH             FALSE )
  set (CMAKE_BUILD_WITH_INSTALL_RPATH     FALSE )
  set (CMAKE_INSTALL_RPATH_USE_LINK_PATH  TRUE  )
endif()

if ( CMAKE_COMPILER_IS_GNUCC )
  add_compile_options (-Wall -Wextra -Wno-unused-result)
  string (REGEX REPLACE "-O3" "-Ofast" CMAKE_C_FLAGS_RELEASE ${CMAKE_C_FLAGS_RELEASE})
endif()
if ( MSVC )
  add_compile_options (/wd4028)
  add_compile_options (/wd4244)
  add_compile_options (/wd4267)
  add_compile_options (/wd4305)
  add_compile_options (/wd4477)
  add_compile_options (/wd4996)
  set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /NODEFAULTLIB:MSVCRTD")
  #set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /NODEFAULTLIB:MSVCRT")
  set (CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

#################################################################
#                         PARSE OPTIONS                         #
#################################################################

if (OMP)
  find_package(OpenMP REQUIRED)
  if (OPENMP_FOUND)
    message(STATUS "OpenMP found")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    if (APPLE)
      list(APPEND linked_libs OpenMP::OpenMP_CXX)
    endif()
  endif()
else()
  message(STATUS "OpenMP disabled")
endif()

if (MSVC)
  add_definitions (-D_CRT_SECURE_NO_DEPRECATE -D_SCL_SECURE_NO_WARNINGS)
endif()

find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)

#################################################################
#                         SETTING DIRECTORIES                   #
#################################################################

set(HPP_DIR    ./cpp/src)
set(INC_DIR    ./cpp/include)
set(EXAMPLE    ./example)
set(OUT_DIR    ./bin)

set(walklib walker)

file(GLOB HPP    "${HPP_DIR}/*.hpp")
file(GLOB HEADER "${INC_DIR}/*.h"  )
file(GLOB EXE    "${EXAMPLE}/*.cpp")
file(GLOB VIEWER "${HPP_DIR}/viewer/*.cpp")

include_directories(${INC_DIR})
include_directories(${HPP_DIR})
include_directories(${INC_DIR}/viewer)

#################################################################
#                          SUMMARY                              #
#################################################################

message(STATUS ""                                                                    )
message(STATUS "=================== Walkers configuration Summary ==================")
message(STATUS "   Walkers version: ${MAJOR}.${MINOR}.${REVISION}"                   )
message(STATUS ""                                                                    )
message(STATUS "   C++ :"                                                            )
message(STATUS "      C++ Compiler : ${CMAKE_CXX_COMPILER}"                          )
message(STATUS "      C++ flags    :"                                                )
foreach(FLAG ${CMAKE_CXX_FLAGS})
  message(STATUS "                    * ${FLAG}"                                     )
endforeach(FLAG)
foreach(FLAG ${CMAKE_CXX_FLAGS_RELEASE})
  message(STATUS "                    * ${FLAG}"                                     )
endforeach(FLAG)
message(STATUS "      Linker flags : "                                               )
foreach(FLAG ${linked_libs})
  message(STATUS "                    * ${FLAG}"                                     )
endforeach(FLAG)
message(STATUS ""                                                                    )
message(STATUS "   OpenMP support : ${OMP}"                                          )
message(STATUS ""                                                                    )

#################################################################
#                         MAIN RULES                            #
#################################################################

add_library(${walklib} SHARED ${HPP} ${HEADER} ${VIEWER})
set_property(TARGET ${walklib} PROPERTY POSITION_INDEPENDENT_CODE ON)
target_link_libraries(${walklib} ${linked_libs})

add_custom_target(test)
add_executable(run ${EXAMPLE}/run.cpp ${HPP})
target_link_libraries(run ${linked_libs} ${walklib} ${OPENGL_gl_LIBRARY} ${OPENGL_glu_LIBRARY} ${GLUT_LIBRARIES})
add_dependencies(test run)

#################################################################
#                          INSTALLERS                           #
#################################################################

install(TARGETS ${walklib}     DESTINATION ${CMAKE_SOURCE_DIR})
install(TARGETS run            DESTINATION ${CMAKE_SOURCE_DIR}/${OUT_DIR})
