# coding: utf-8
import sys

from typing import Tuple

"""
Github: https://github.com/czasg/CommandController
Install: pip install command-controller
"""

__version__ = "0.0.1"


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
            assert flag, f"flag[{flag}] invalid"
            assert flag.strip("-") != "", f"flag[{flag}] invalid"
            assert flag.startswith("-"), f"flag[{flag}] is invalid, it should be startswith `-`."
        self.flags = flags
        self.prefetch = prefetch
        self.default = default
        self.enum = enum
        self.require = require
        self.description = description
        self.v = default
        self.has_been_configured = False

    def options(self):
        short_flag, long_flag = [], []
        for flag in self.flags:
            if flag.startswith("--"):
                long_flag.append(flag)
            elif flag.startswith("-"):
                short_flag.append(flag)
        typ = f"[{self.typ()}]"
        required = "[require]" if self.require else ""
        default = f"[default:{self.default}]" if self.default else ""
        description = self.description if self.description else ""
        return short_flag, long_flag, typ, required, default, description

    def __str__(self):
        short_flag, long_flag, typ, required, default, description = self.options()
        return f"{short_flag} {long_flag} {typ} {required} {default}    {description}"

    def value(self):
        raise NotImplemented

    def typ(self) -> str:
        return "string"

    def set_value(self, v) -> None:
        self.has_been_configured = True


class FlagInt(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    def value(self) -> int:
        return self.v or 0

    def typ(self) -> str:
        return "int"

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

    def typ(self) -> str:
        return "string"

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

    def typ(self) -> str:
        return "bool"

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

    def typ(self) -> str:
        return "list"

    def set_value(self, v):
        if not self.v:
            self.v = []
        if isinstance(v, (str, int)):
            self.v.append(v)
        elif isinstance(v, (tuple, list)):
            self.v += v[1:]
        else:
            raise Exception(f"Invalid Flag Value: {v}")
        super().set_value(v)


class FlagMap(Flag):

    def __init__(self, flags, prefetch=1, sep="=", *args, **kwargs):
        super().__init__(flags, *args, prefetch=prefetch, **kwargs)
        self.sep = sep

    def value(self) -> dict:
        return self.v or dict()

    def typ(self) -> str:
        return "map"

    def set_value(self, v):
        if not self.v:
            self.v = dict()
        if isinstance(v, (tuple, list)):
            v = v[1]
        if isinstance(v, str) and self.sep in v:
            key, val = v.split(self.sep, 1)
            self.v[key] = val
        else:
            raise Exception(f"Invalid Flag Value: {v}")
        super().set_value(v)


class Command:

    def __init__(self):
        self.sub_commands = {}
        self.sub_command_links = []

    class flags:
        ...

    def help(self, exit=None):
        if self.usages():
            print("----------------")
            print(f"Usage:")
            print(f"  {self.usages()}")
        if self.descriptions():
            print("----------------")
            print("Descriptions:")
            print(f"  {self.descriptions()}")
        if self.sub_command_links:
            print("----------------")
            print("Commands:")
            max_entrypoint_length = 0
            for command in self.sub_command_links:
                max_entrypoint_length = max(max_entrypoint_length, len(command.entrypoints()))
            for command in self.sub_command_links:
                entrypoints = command.entrypoints()
                entrypoints = fix_empty_space(entrypoints, max_entrypoint_length)
                descriptions = command.descriptions()
                print(f"  {entrypoints}    {descriptions}")
        if [flag for name, flag in vars(self.flags).items() if isinstance(flag, Flag)]:
            print("----------------")
            print("Options:")
            max_short_flag_length = 0
            max_long_flag_length = 0
            max_typ_length = 0
            max_required_length = 0
            max_default_length = 0
            options = []
            for name, flag in vars(self.flags).items():
                if not isinstance(flag, Flag):
                    continue
                options.append(flag.options())
                short_flag, long_flag, typ, required, default, description = flag.options()
                max_short_flag_length = max(max_short_flag_length, len(" ".join(short_flag)))
                max_long_flag_length = max(max_long_flag_length, len(" ".join(long_flag)))
                max_typ_length = max(max_typ_length, len(typ))
                max_required_length = max(max_required_length, len(required))
                max_default_length = max(max_default_length, len(default))
            for short_flag, long_flag, typ, required, default, description in options:
                short_flag_text = fix_empty_space(" ".join(short_flag), max_short_flag_length)
                long_flag_text = fix_empty_space(" ".join(long_flag), max_long_flag_length)
                typ = fix_empty_space(typ, max_typ_length)
                required = fix_empty_space(required, max_required_length)
                default = fix_empty_space(default, max_default_length)
                print(f"  {short_flag_text} {long_flag_text} {typ} {required} {default}    {description}")
        if exit is not None:
            sys.exit(exit)

    def entrypoints(self) -> str:
        name = self.__class__.__name__.lower()
        if name.endswith("command"):
            name = name[:-7]
        elif name.endswith("cmd"):
            name = name[:-3]
        return name

    def usages(self) -> str:
        if self.entrypoints():
            return f"{self.entrypoints()} [OPTIONS]"
        return ""

    def descriptions(self) -> str:
        return ""

    def add(self, *commands):
        for command in commands:
            if type(command) == type:
                command = command()
            assert isinstance(command, Command), f"{command} typ err"
            assert command.entrypoints(), f"{command} entrypoint is empty"
            assert command.entrypoints() not in self.sub_commands, f"{command} deplicate define."
            self.sub_commands[command.entrypoints()] = command
            self.sub_command_links.append(command)
        return self

    def run(self, *args):
        pass


def NewCommand() -> Command:
    return Command()


def parse_entrypoints_flags_from_argv() -> Tuple[list, list]:
    # entrypoints
    argv = sys.argv[1:]
    entrypoints = []
    for arg in argv:
        if arg.startswith("-"):
            break
        entrypoints.append(arg)
    # parse flags
    flags = argv[len(entrypoints):]
    return entrypoints, flags


def Execute(cmd: Command):
    # first command entrypoint should be empty.
    if cmd.entrypoints():
        cmd = NewCommand().add(cmd)
    # parse sys args.
    entrypoints, flags = parse_entrypoints_flags_from_argv()
    if not entrypoints:
        print("empty entrypoint, please see --help.")
        cmd.help(1)
    # parse entrypoint command.
    for entrypoint in entrypoints:
        if entrypoint not in cmd.sub_commands:
            print(f"not found entrypoint[{entrypoint}], please see --help.")
            cmd.help(1)
        cmd = cmd.sub_commands[entrypoint]
    # check help.
    for flagName in flags:
        if flagName in ("-h", "--help"):
            cmd.help(0)
    # verify command flag map.
    flagInsMap = {}
    for flagInsName, flagIns in vars(cmd.flags).items():
        if not isinstance(flagIns, Flag):
            continue
        for flagName in flagIns.flags:
            if flagName in flagInsMap:
                print(f"command property[flags.{flagInsName}] duplicate flagName[{flagName}]")
                sys.exit(1)
            flagInsMap[flagName] = flagIns
    # parse & set flag value
    index = 0
    while index < len(flags):
        flagName = flags[index]
        flagName = flagName.strip()
        if flagName.startswith("-"):
            # parse value
            if "=" in flagName:
                props = [tuple(flagName.split("=", 1))]
            elif flagName.startswith("--"):
                props = [(flagName, None)]
            elif flagName.startswith("-"):
                props = [(f"-{f}", None) for f in flagName.strip("-")]
            else:
                print(f"unsupported flag[{flagName}] yet.")
                sys.exit(1)
            # set value
            for flagName, flagValue in props:
                if flagName not in flagInsMap:
                    print(f"undefined flag[{flagName}].")
                    cmd.help(1)
                flagIns: Flag = flagInsMap[flagName]
                values = [flagName]
                prefetch = flagIns.prefetch
                while prefetch > 0:
                    prefetch -= 1
                    if flagValue is None:
                        index += 1
                        if index > len(flags):
                            print(f"flag[{flagName}] need {flagIns.prefetch} value, but 0 given.")
                            cmd.help(1)
                        flagValue = flags[index]
                    if flagValue in flagInsMap:
                        print(f"flag[{flagName}] need {flagIns.prefetch} value, but next is flag[{flagValue}]")
                        cmd.help(1)
                    values.append(flagValue)
                    flagValue = None
                flagIns.set_value(values)
            index += 1
            continue
        break
    # check require flags
    for flagInsName, flagIns in flagInsMap.items():
        if flagIns.require and not flagIns.has_been_configured:
            print(f"flag[{flagInsName}] is require.")
            cmd.help(1)
    # start with args
    cmd.run(*flags[index:])
