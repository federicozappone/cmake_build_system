cmake_minimum_required(VERSION 3.25)
get_filename_component(module_name ${CMAKE_CURRENT_LIST_DIR} NAME)
string(REPLACE " " "_" module_name ${module_name})


set(SANDBOX_PKGS_DIR ${CMAKE_CURRENT_LIST_DIR}/../../pkgs)
set(SANDBOX_INCLUDE_DIR ${CMAKE_CURRENT_LIST_DIR}/../../include)
set(SANDBOX_LIB_DIR ${CMAKE_CURRENT_LIST_DIR}/../../lib)
set(SANDBOX_BIN_DIR ${CMAKE_CURRENT_LIST_DIR}/../../bin)


link_directories(${SANDBOX_LIB_DIR})
include_directories(${SANDBOX_INCLUDE_DIR})

set(CFLAGS "")
set(LFLAGS "")


if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/Makefile")
  include(${CMAKE_CURRENT_LIST_DIR}/Makefile)
endif()

if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/module.deps")
  include(${CMAKE_CURRENT_LIST_DIR}/module.deps)
endif()


if(DEFINED INC_LINKS AND NOT INC_LINKS STREQUAL "")
  foreach(file ${INC_LINKS})
    message("Creating symlink for ${file} inside ${SANDBOX_INCLUDE_DIR}")
    execute_process(
      COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_CURRENT_LIST_DIR}/${file} ${SANDBOX_INCLUDE_DIR}/${file}
    )
  endforeach()
endif()



set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CFLAGS} ${LFLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${LFLAGS}")



set(DIRECTORY_TO_LIST "${SANDBOX_PKGS_DIR}")
file(GLOB pkgs RELATIVE ${DIRECTORY_TO_LIST} ${DIRECTORY_TO_LIST}/*)


if(DEFINED LIB_SRCS AND NOT LIB_SRCS STREQUAL "")
  add_library(${module_name} SHARED ${LIB_SRCS})
  target_include_directories(${module_name} PUBLIC ${SANDBOX_INCLUDE_DIR})

  set(FILTERED_DEPS ${MOD_DEPS})
  list(REMOVE_ITEM FILTERED_DEPS ${module_name})

  target_link_libraries(${module_name} ${FILTERED_DEPS})

  add_custom_command(TARGET ${module_name} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E create_symlink $<TARGET_FILE:${module_name}> "${SANDBOX_LIB_DIR}/lib${module_name}.so"
  )
endif()


if(DEFINED BIN_SRCS AND NOT BIN_SRCS STREQUAL "")
  foreach(file ${BIN_SRCS})
    get_filename_component(executable_name ${file} NAME_WE)
    add_executable(${executable_name} ${file})

    target_include_directories(${executable_name} PUBLIC ${SANDBOX_INCLUDE_DIR})
    target_link_libraries(${executable_name} ${MOD_DEPS})

    foreach(pkg ${pkgs})
      file(GLOB PKG_LIBRARIES "${SANDBOX_LIB_DIR}/lib${pkg}*.so")
      target_link_libraries(${executable_name} ${PKG_LIBRARIES})

      if (${pkg} MATCHES "opencv")
        # workaround because opencv doesn't install headers directly in the opencv2 folder
        include_directories(${CMAKE_CURRENT_LIST_DIR}/../../include/opencv4)
      endif()

    endforeach()

  file(MAKE_DIRECTORY "${SANDBOX_BIN_DIR}/${module_name}")
    add_custom_command(TARGET ${executable_name} POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E create_symlink $<TARGET_FILE:${executable_name}> "${SANDBOX_BIN_DIR}/${module_name}/${executable_name}"
    )
  endforeach()
endif()
