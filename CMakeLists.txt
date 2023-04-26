cmake_minimum_required(VERSION 3.21)
project(sandbox)

include(ExternalProject)

file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/include")
file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/lib")
file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/bin")
file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/pkgs")
file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/src")
file(MAKE_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/build")

execute_process(COMMAND python3 "${CMAKE_CURRENT_LIST_DIR}/make/generate_moddeps.py")

set(pkgs_dir "${CMAKE_CURRENT_LIST_DIR}/pkgs")
file(GLOB pkgs RELATIVE ${pkgs_dir} ${pkgs_dir}/*)
message("List of packages: ${pkgs}")

set(SANDBOX_INSTALL_LOCATION ${CMAKE_CURRENT_LIST_DIR})

foreach(pkg ${pkgs})
  ExternalProject_Add(${pkg}
    SOURCE_DIR ${pkgs_dir}/${pkg}
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${SANDBOX_INSTALL_LOCATION}
  )

endforeach()

set(modules_dir "${CMAKE_CURRENT_LIST_DIR}/src")

file(GLOB modules RELATIVE ${modules_dir} ${modules_dir}/*)

foreach(module ${modules})
  if(IS_DIRECTORY "${modules_dir}/${module}")
    message("Adding module: ${module}")
    file(COPY ${CMAKE_CURRENT_LIST_DIR}/make/CMakeLists.txt DESTINATION ${modules_dir}/${module})
    add_subdirectory("${modules_dir}/${module}")
  endif()
endforeach()
