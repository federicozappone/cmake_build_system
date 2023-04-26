import sys
import os


if len(sys.argv) != 2:
    print("Usage: make_module.py [module_name]")
    exit(-1)

sandbox_root = os.environ.get("SANDBOX_ROOT")

if sandbox_root is None or sandbox_root == "":
    print("SANDBOX_ROOT not set")
    exit(-1)

print("SANDBOX_ROOT:", os.environ.get("SANDBOX_ROOT"))

module_path = os.environ.get("SANDBOX_ROOT") + f"/src/{sys.argv[1]}"
print("New module path:", module_path)

if os.path.exists(module_path):
    print("A module with that name already exists")
    exit(-1)

os.mkdir(module_path)

with open(f"{module_path}/Makefile", "w") as f:
    f.write('set(LIB_SRCS "")\nset(INC_LINKS "")\nset(BIN_SRCS "")')
    f.close()
