import subprocess

def find_libs():

    f = open("/proc/self/maps", "rt")
    lines = f.readlines()
    f.close()
    set_of_libs = set()

    for line in lines:
        if line.find(".so") == -1:
            continue

        i = line.find(" ")
        if i < 0:
            continue
        line = line[i + 1 :]
        i = line.find(" ")
        if i < 0:
            continue
        line = line[i + 1 :]
        i = line.find(" ")
        if i < 0:
            continue
        line = line[i + 1 :]
        i = line.find(" ")
        if i < 0:
            continue
        line = line[i + 1 :]
        i = line.find(" ")
        if i < 0:
            continue
        line = line[i + 1 :]

        soname = line.lstrip().rstrip("\n")
        set_of_libs.add(soname)

    return set_of_libs

symbol_map = {}

def is_system_library(libname):
    return "/ld-" in libname or "/libc-" in libname or "/libm-" in libname or "/libpthread-" in libname or "libkrb5.so" in libname or "libgssapi.so" in libname or "libresolv-" in libname or "libbsd.so" in libname

for libname in find_libs():

    ret = subprocess.run(["objdump", "-T", libname], capture_output=True)
    for l in ret.stdout.decode("ascii").split("\n"):
        if "DF .text" in l:
            symbol_name = l.split(" ")[-1]
            if not symbol_name.startswith("_Z"):
                if symbol_name not in symbol_map:
                    symbol_map[symbol_name] = libname
                else:
                    other_libname = symbol_map[symbol_name]
                    if libname != other_libname and not (is_system_library(libname) and is_system_library(other_libname)):
                        print("WARNING: %s present in %s is also present in %s" % (symbol_name, libname, other_libname))

