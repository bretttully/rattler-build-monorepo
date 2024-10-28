# libs/lib2/CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(nm_c_extensions)

# Find Python and add pybind11
find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Add the extension module
pybind11_add_module(libnm_c cpp/libnm_c.cpp)

# Set the output directory to the Python package directory
set_target_properties(libnm_c PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/nm_c"
)

# Enable position independent code
set_target_properties(libnm_c PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Optional: Add optimization flags for Release builds
target_compile_options(libnm_c PRIVATE
    $<$<CONFIG:Release>:-O3>
    $<$<CONFIG:Release>:-march=native>
)