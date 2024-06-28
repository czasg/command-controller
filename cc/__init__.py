# coding: utf-8
import sys

from typing import Tuple


def to_bool(value):
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ('yes', 'true', 't', '1', 'ok'):
            return True
        elif value in ('no', 'false', 'f', '0'):
            return False
    elif isinstance(value, int):
        return value != 0
    return False


def fix_empty_space(v: str, length: int):
    if len(v) < length:
        v += " " * (length - len(v))
    return v


class Flag:

    def __init__(self, flags: list,
                 prefetch=0,
                 default=None,
                 enum=None,
                 require=False,
                 description=None,
                 ):
        if not flags:
            raise Exception(f"{self.__name__} need define flags.")
        for flag in flags:
            if not flag.startswith("-"):
                raise Exception(f"flag[{flag}] is invalid, it should be startswith `-`.")
        self.flags = flags
        self.prefetch = prefetch
        self.default = default
        self.enum = enum
        self.require = require
        self.description = description
        self.v = default
        self.__done__ = False

    def options(self):
        short_flag, long_flag = [], []
        for flag in self.flags:
            if flag.startswith("--"):
                long_flag.append(flag)
            elif flag.startswith("-"):
                short_flag.append(flag)
        required = "[require]" if self.require else ""
        default = f"[default:{self.default}]" if self.default else ""
        description = self.description if self.description else ""
        return short_flag, long_flag, required, default, description
        # flag = self.flags[:]
        # if self.prefetch == 1:
        #     flag.append("string")
        # elif self.prefetch > 1:
        #     flag.append("list")
        # if self.require:
        #     flag.append("[require]")
        # option = " ".join(flag)
        #
        # desc = []
        # if self.description:
        #     desc.append(self.description)
        # if self.default is not None:
        #     desc.append(f"(default: {self.default})")
        # description = "\n".join(desc)
        # return option, description

    def __str__(self):
        short_flag, long_flag, required, default, description = self.options()
        return f"{short_flag} {long_flag} {required} {default}    {description}"

    def value(self):
        raise NotImplemented

    def set_value(self, v):
        self.__done__ = True


class FlagInt(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    def value(self) -> int:
        return self.v or 0

    def set_value(self, v):
        if isinstance(v, (str, int)):
            self.v = int(v)
        elif isinstance(v, (tuple, list)):
            if len(v) <= 1:
                raise Exception("empty flag value")
            if len(v) > 2:
                raise Exception(f"flag need only one value, but {len(v) - 1} were given")
            self.v = int(v[1])
        else:
            raise Exception(f"Invalid Flag Value: {v}")
        super().set_value(v)


class FlagStr(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, *args, prefetch=prefetch, **kwargs)

    def value(self) -> str:
        return self.v or ""

    def set_value(self, v):
        if isinstance(v, (str, int)):
            self.v = str(v)
        elif isinstance(v, (tuple, list)):
            if len(v) <= 1:
                raise Exception("empty flag value")
            if len(v) > 2:
                raise Exception(f"flag need only one value, but {len(v) - 1} were given")
            self.v = str(v[1])
        else:
            raise Exception(f"Invalid Flag Value: {v}")
        super().set_value(v)


class FlagBool(Flag):

    def __init__(self, flags, prefetch=0, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    def value(self) -> bool:
        return self.v or False

    def set_value(self, v):
        if isinstance(v, bool):
            self.v = v
        elif isinstance(v, (str, int)):
            self.v = to_bool(v)
        elif isinstance(v, (tuple, list)):
            if len(v) <= 1:
                self.v = True
            if len(v) > 2:
                raise Exception(f"flag need only one value, but {len(v) - 1} were given")
            if len(v) == 2:
                self.v = to_bool(v[1])
        else:
            raise Exception(f"Invalid Flag Value: {v}")
        super().set_value(v)


class FlagList(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, *args, prefetch=prefetch, **kwargs)

    def value(self) -> list:
        return self.v or []

    def set_value(self, v):
        if isinstance(v, (str, int)):
            self.v = [v]
        elif isinstance(v, (tuple, list)):
            if len(v) <= 1:
                self.v = []
            else:
                self.v = v[1:]
        else:
            raise Exception(f"Invalid Flag Value: {v}")
        super().set_value(v)


class Command:

    def __init__(self):
        self.sub_commands = {}
        self.sub_command_links = []
        self.entrypoint = None
        self.description = None

    class flags:
        ...

    def help(self, exit=None):
        if self.descriptions():
            print("----------------")
            print("Descriptions:")
            print(self.descriptions())
        if self.sub_command_links:
            print("----------------")
            print("Commands:")
            max_entrypoint_length = 0
            for command in self.sub_command_links:
                max_entrypoint_length = max(max_entrypoint_length, len(', '.join(command.entrypoints())))
            for command in self.sub_command_links:
                entrypoints = ', '.join(command.entrypoints())
                entrypoints = fix_empty_space(entrypoints, max_entrypoint_length)
                descriptions = command.descriptions()
                print(f"  {entrypoints}    {descriptions}")
        if [flag for name, flag in vars(self.flags).items() if isinstance(flag, Flag)]:
            print("----------------")
            print("Options:")
            max_short_flag_length = 0
            max_long_flag_length = 0
            max_required_length = 0
            max_default_length = 0
            options = []
            for name, flag in vars(self.flags).items():
                if not isinstance(flag, Flag):
                    continue
                short_flag, long_flag, required, default, description = flag.options()
                options.append((short_flag, long_flag, required, default, description))
                max_short_flag_length = max(max_short_flag_length, len(" ".join(short_flag)))
                max_long_flag_length = max(max_long_flag_length, len(" ".join(long_flag)))
                max_required_length = max(max_required_length, len(required))
                max_default_length = max(max_default_length, len(default))
            for short_flag, long_flag, required, default, description in options:
                short_flag_text = fix_empty_space(" ".join(short_flag), max_short_flag_length)
                long_flag_text = fix_empty_space(" ".join(long_flag), max_long_flag_length)
                required = fix_empty_space(required, max_required_length)
                default = fix_empty_space(default, max_default_length)
                print(f" {short_flag_text} {long_flag_text} {required} {default}    {description}")
        if exit is not None:
            sys.exit(exit)

    def entrypoints(self) -> [str]:
        name = self.__class__.__name__.lower()
        if name.endswith("command"):
            name = name[:-7]
        elif name.endswith("cmd"):
            name = name[:-3]
        return [name] if name else []

    def descriptions(self) -> str:
        return ""

    def add(self, *commands):
        for command in commands:
            if type(command) == type:
                command = command()
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


def parse_entrypoints_flags_from_argv() -> Tuple[list, list]:
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
        arg = arg.strip()
        if arg.startswith("-") and flag:
            flags.append(flag)
        # long flag
        if arg.startswith("--"):
            long_flag = arg
            # check long flag
            if not long_flag.strip("-"):
                print(f"empty long flag[{long_flag}]")
                sys.exit(1)
            # parse long flag
            if "=" in long_flag:
                flag = long_flag.split("=", 1)
            else:
                flag = [long_flag]
            continue
        # short flag
        elif arg.startswith("-"):
            short_flag = arg
            # check short flag
            if "=" in short_flag:
                print(f"invalid flag[{short_flag}], please use ` ` replace `=`")
                sys.exit(1)
            short_flag = short_flag.strip().strip("-")
            if len(short_flag) == 1:
                flag = [f"-{short_flag}"]
            elif len(short_flag) > 1:
                for f in short_flag[:-1]:
                    flags.append([f"-{f}"])
                flag = [f"-{short_flag[-1]}"]
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
            cmd.help(1)
        cmd = cmd.sub_commands[entrypoint]

    # check help
    for flagItem in flags:
        flagName = flagItem[0]
        if flagName in ("-h", "--help"):
            cmd.help(0)

    for flagItem in flags:
        flagName = flagItem[0]
        flagFound = None
        for name, flag in vars(cmd.flags).items():
            if not isinstance(flag, Flag):
                continue
            if flagName not in flag.flags:
                continue
            # set value
            try:
                flag.set_value(flagItem)
            except Exception as e:
                print(f"flag[{name}] parse error[{e}].")
                cmd.help(1)
            flagFound = flag
            break
        # not found flag
        if not flagFound:
            print(f"flag[{flagName}] is not defined")
            cmd.help(1)
            return

    # check required
    for name, flag in vars(cmd.flags).items():
        if not isinstance(flag, Flag):
            continue
        if flag.require and not flag.__done__:
            print(f"flag[{name}] is required.")
            cmd.help(1)

    cmd.run()
