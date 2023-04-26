# Simple CMake-based Build System

This is a very simple build and sandboxing system that automatically takes care of inter-module dependencies and external packages (only external project that use cmake as build system are supported).\
The system also uses python to compute dependencies and for various utilities.

This will allow you to quickly write code, create modules with libraries and executables and make use of external libraries without having to write any makefile or take care of dependencies yourself.


## Quick start

Clone the build system
```
git clone https://github.com/federicozappone/cmake_build_system.git sandbox
cd sandbox
```

Install Python scripts requirements
```
pip install -r requirements.txt
```


Set required enviromental variable
```
export SANDBOX_ROOT=$(pwd)
```

Do a dry run to initialize the folders structure
```
cd $(SANDBOX_ROOT)/build
cmake ..
```

Clone external modules in the ```pkgs``` directory (example with opencv and gtsam)
```
cd $(SANDBOX_ROOT)/pkgs
git clone https://github.com/opencv/opencv.git
git clone https://github.com/borglab/gtsam.git
```

Create your first modules
```
cd $(SANDBOX_ROOT)
python make/make_module.py matrices
```

You will have a new empty module in the ```src``` folder of the sandbox root.
Inside you will find a ```Makefile``` file where you will only need to add the list of headers, library sources and executable sources of your module.

Example
```
set(LIB_SRCS "matrix.cpp" "svd.cpp")
set(INC_LINKS "matrix.h" "svd.h")
set(BIN_SRCS "test_matrix.cpp")
```

Your new module folder structure will look like this

    src
    ├── ...
    ├── matrices
    │   ├── Makefile
    │   ├── matrix.h
    │   ├── matrix.cpp
    │   ├── svd.h
    │   ├── svd.cpp
    │   └── test_matrix.cpp
    └── ...

Go ahead and create more modules without worrying about cross module or third-party packages dependencies.\
You can also use the cloned packages in your modules without having to specify extra links or directories.

Build the sandbox
```
cd $(SANDBOX_ROOT)/build
cmake ..
make
```

Note: the first run will also build all the packages and it might take a while.

Executables for a given module can be found inside the ```bin``` folder.
Symlinks for generated libraries and headers are also available in the ```lib``` and ```include``` folders respectively.


## Module Makefile Customization

You can add extra "cmake-instructions" inside the module Makefile, for instance
```
set(LIB_SRCS "matrix.cpp" "svd.cpp")
set(INC_LINKS "matrix.h" "svd.h")
set(BIN_SRCS "test_matrix.cpp")

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -ggdb")
```

## Packages Handling and Dependecies

Imported external packages will be built and avaialble only locally inside the sandbox and will not be installed system-wide.
The build system will not install extra system dependencies needed by the packages, hence, the user will have to pre-install any requirement for a given project.
