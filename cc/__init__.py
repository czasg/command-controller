# coding: utf-8
import sys

from typing import Tuple

empty_space = 4

class Flag:

    def __init__(self, flags: list,
                 prefetch=0,
                 default=None,
                 enum=None,
                 require=False,
                 description=None,
                 ):
        self.flags = flags
        self.prefetch = prefetch
        self.default = default
        self.enum = enum
        self.require = require
        self.description = description
        self.v = default

    def options(self) -> Tuple[str, str]:
        flag = self.flags[:]
        if self.prefetch == 1:
            flag.append("string")
        elif self.prefetch > 1:
            flag.append("list")
        if self.require:
            flag.append("[require]")
        option = " ".join(flag)

        desc = []
        if self.description:
            desc.append(self.description)
        if self.default is not None:
            desc.append(f"(default: {self.default})")
        description = "\n".join(desc)
        return option, description

    def __str__(self):
        option, description = self.options()
        descriptions = description.split("\n")
        desc = descriptions[0]
        for description in descriptions[1:]:
            desc += "\n"
            desc += " " * (len(option) + empty_space)
            desc += description
        return f"{option}{' '*empty_space}{desc}"


class FlagInt(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    @property
    def value(self) -> int:
        return self.v

    @value.setter
    def value(self, v: int):
        # assert isinstance(v, int), "invalid int value, see --help"
        self.v = int(v)

    # def __add__(self, v):
    #     return self.value + v
    #
    # def __sub__(self, v):
    #     return self.value - v


class FlagStr(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, *args, prefetch=prefetch, **kwargs)

    @property
    def value(self) -> str:
        return self.v

    @value.setter
    def value(self, v: str):
        assert isinstance(v, str), "invalid int value, see --help"
        self.v = v


class FlagBool(Flag):

    def __init__(self, flags, prefetch=0, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    @property
    def value(self) -> bool:
        return self.v

    @value.setter
    def value(self, v: bool):
        assert isinstance(v, bool), "invalid int value, see --help"
        self.v = v

    def __bool__(self):
        return self.value


class Command:

    def __init__(self):
        self.sub_commands = {}
        self.sub_command_links = []

        self.flag_pool = {}
        for flag in dir(self.flags):
            pass
        """
        每一个 command 都需要把 flags 的属性解析出来。
        1. 方便 args 解析
        2. 方便 help 输出
        """

    class flags:
        ...

    def help(self):
        max_option_length = 0
        options = []
        for name, flag in vars(self.flags).items():
            if not isinstance(flag, Flag):
                continue
            option, description = flag.options()
            options.append((option, description))
            max_option_length = max(max_option_length, len(option))
        text = []
        text.append("Options:")
        for option, description in options:
            descriptions = description.split("\n")
            desc = descriptions[0]
            for description in descriptions[1:]:
                desc += "\n"
                desc += " " * (max_option_length+ empty_space)
                desc += description
            text.append(f"{option}{' ' * (empty_space+max_option_length-len(option))}{desc}")
        print("\n".join(text))



    def entrypoints(self) -> [str]:
        name = self.__class__.__name__.lower()
        if name.endswith("command"):
            name = name[:-7]
        elif name.endswith("cmd"):
            name = name[:-3]
        return [name] if name else []

    def descriptions(self) -> [str]:
        return [
            f"use by {self.entrypoints()}",
        ]

    def add(self, *commands):
        for command in commands:
            assert isinstance(command, Command), f"{command} typ err"
            assert command.entrypoints(), f"{command} entrypoint is empty"
            for entrypoint in command.entrypoints():
                if entrypoint in self.sub_commands:
                    print("--help")
                    sys.exit(1)
                self.sub_commands[entrypoint] = command
            self.sub_command_links.append(command)
        return self

    def run(self):
        pass


def NewCommand() -> Command:
    return Command()


def is_flag(s: str) -> bool:
    return s.startswith("-")

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

def Execute(cmd: Command):
    if cmd.entrypoints():
        cmd = NewCommand().add(cmd)

    entrypoints, flags = parse_entrypoints_flags_from_argv()

    for entrypoint in entrypoints:
        if entrypoint not in cmd.sub_commands:
            cmd.help()
            sys.exit(1)
        cmd = cmd.sub_commands[entrypoint]

    for flagItem in flags:
        flagName = flagItem[0]
        flagFound = None
        for name, flag in vars(cmd.flags).items():
            if flagName not in flag.flags:
                continue
            # set value
            flag.v = flagItem[1]
            flagFound = flag
            break
        # not found flag
        if not flagFound:
            return


    # args = sys.argv[1:]
    # if not args:
    #     print("--help not entrypoint")
    #     cmd.help()
    #     sys.exit(1)
    # print(sys.argv)

    """
    前面几个必须是有序的 command，不然无法找到。
    需要先找到，然后再验证 后面的参数是否符合预期。
    """
    # entrypoint_index = 0
    # for entrypoint in args:
    #     if entrypoint.startswith("-"):
    #         break
    #     if entrypoint not in cmd.sub_commands:
    #         print(f"--help, unknown {entrypoint}")
    #         cmd.help()
    #         sys.exit(1)
    #     cmd = cmd.sub_commands[entrypoint]
    #     entrypoint_index += 1
    #
    # print(f"found cmd {cmd}")

    # # 解析 cmd flag
    # short_flag = {}
    # long_flag = {}
    # for name, flag in vars(cmd.flags).items():
    #     if not isinstance(flag, Flag):
    #         continue
    #     # print([name, flag])
    #     # _ = flag.flags
    #     for _flag in flag.flags:
    #         if _flag.startswith("--"):
    #             long_flag[_flag] = flag
    #         elif _flag.startswith("-"):
    #             for __flag in _flag.strip("-"):
    #                 short_flag[f"-{__flag}"] = flag
    #         else:
    #             print("--help, flags invalid")
    #             sys.exit(1)
    # print(f"short_flag={short_flag}")
    # print(f"long_flag={long_flag}")
    #
    # # 匹配命中
    # print(args[entrypoint_index:])
    # flags = args[entrypoint_index:]
    """
    不需要支持等于号，意义不大
    """
    # index = 0
    # while index < len(flags):
    #     flag_str = flags[index]
    #     if flag_str.startswith("--"):
    #         # if "=" in flag_str:
    #         #     flag, value = flag_str.split("=", 1)
    #         assert flag_str in long_flag, f"flag[{flag_str}] not found, please see --help"
    #         flag = long_flag[flag_str]
    #         prefetch = flag.prefetch
    #         while prefetch > 0:
    #             prefetch -= 1
    #             # print(flags[index + 1], "??", index)
    #             if is_flag(flags[index + 1]):
    #                 if flag.require:
    #                     print(f"{flag_str} is required see --help")
    #                     sys.exit(1)
    #                 break
    #             # 赋值
    #             flag.value = flags[index + 1]
    #             print(flag.value)
    #             index += 1
    #     elif flag_str.startswith("-"):
    #         for flag_str in flag_str.strip("-").split():
    #             flag_str = f"-{flag_str}"
    #             assert flag_str in short_flag, f"flag[{flag_str}] not found, please see --help"
    #             flag = short_flag[flag_str]
    #             prefetch = flag.prefetch
    #             # print(flag_str, prefetch, is_flag(flags[index + 1]))
    #             while prefetch > 0:
    #                 prefetch -= 1
    #                 # print(flags[index + 1], "??", index)
    #                 if is_flag(flags[index + 1]):
    #                     if flag.require:
    #                         print(f"{flag_str} is required see --help")
    #                         sys.exit(1)
    #                     break
    #                 print(flag.value, "!!!")
    #                 flag.value = flags[index + 1]
    #                 print(flag.value, "???")
    #             index += 1
    #     else:
    #         print(f"invalid flag {flag_str} --help")
    #         sys.exit(1)
    #     index += 1
    #
    # for name, flag in vars(cmd.flags).items():
    #     if not isinstance(flag, Flag):
    #         continue
    #     print([name, flag.value])
    #
    # cmd.run()
