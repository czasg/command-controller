# codingL utf-8
import sys


def parse_entrypoints_flags_from_argv() -> (list, list):
    argv = sys.argv[1:]
    entrypoints = []
    for arg in argv:
        if arg.startswith("-"):
            break
        entrypoints.append(arg)

    if not entrypoints:
        sys.exit(1)

    argv = argv[len(entrypoints):]
    flags = []
    flag = []
    for arg in argv:
        if arg.startswith("-"):
            if flag:
                flags.append(flag)
            flag = [arg]
            continue
        flag.append(arg)
    if flag:
        flags.append(flag)
    return entrypoints, flags


if __name__ == '__main__':
    entrypoints, flags = parse_entrypoints_flags_from_argv()
    print(entrypoints)
    print(flags)
