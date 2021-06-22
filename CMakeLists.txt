cmake_minimum_required(VERSION 3.16.3)
project(wks)

set(BUILD_SHARED_LIBS ON) 

option(ENABLE_TESTING "Enable unit tests" OFF)

# Libs are in lib/ and binaries in bin/
include(GNUInstallDirs)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})

#Enable real warnings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wpedantic")

# Enable open mp support
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")

# Enable common instruction set
add_compile_options(-mavx -msse2)

include(CTest)
add_subdirectory(src)
