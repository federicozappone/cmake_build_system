import os
import CppHeaderParser


print("Generating moddeps")

sandbox_root = os.environ.get("SANDBOX_ROOT")

if sandbox_root is None or sandbox_root == "":
    print("generate_moddeps SANDBOX_ROOT not set")
    exit(-1)

print("SANDBOX_ROOT:", os.environ.get("SANDBOX_ROOT"))


module_dict = {}
module_deps = {}


for path, subdirs, files in os.walk(f"{sandbox_root}/src"):
    module_name = path.split("/")[-1]
    module_deps[module_name] = []

    for file_name in files:
        if (file_name.endswith(".h")):
            module_dict[file_name] = module_name


for path, subdirs, files in os.walk(f"{sandbox_root}/src"):
    module_name = path.split("/")[-1]

    for file_name in files:
        if (file_name.endswith(".h")) or (file_name.endswith(".cpp")) or (file_name.endswith(".cc")):
            headers = CppHeaderParser.CppHeader(os.path.join(path, file_name))

            for incl in headers.includes:
                if incl[1:-1] in module_dict:
                    if module_dict[incl[1:-1]] not in module_deps[module_name]:
                        module_deps[module_name].append(module_dict[incl[1:-1]])


module_deps.pop("src")


for module in module_deps:
    deps_string = 'set(MOD_DEPS'
    for dep in module_deps[module]:
        deps_string += f' "{dep}"'
    deps_string += ')'

    with open(f"{sandbox_root}/src/{module}/module.deps", "w") as deps_file:
        deps_file.write(deps_string)
