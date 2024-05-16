# coding: utf-8

class Flag:

    def __init__(self, flags: list,
                 prefetch=0,
                 default=None,
                 enum=None,
                 require=False,
                 descriptions=None,
                 ):
        self.flags = flags
        self.prefetch = prefetch
        self.default = default
        self.enum = enum
        self.require = require
        self.descriptions = descriptions


class FlagInt(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    def value(self) -> int:
        return 99999


class FlagStr(Flag):

    def __init__(self, flags, prefetch=1, *args, **kwargs):
        super().__init__(flags, *args, prefetch=prefetch, **kwargs)

    def value(self) -> str:
        return "?????"


class FlagBool(Flag):

    def __init__(self, flags, prefetch=0, *args, **kwargs):
        super().__init__(flags, prefetch=prefetch, *args, **kwargs)

    def value(self) -> bool:
        return False

    def __bool__(self):
        return self.value()


class InitCommand:
    # command
    alias = ["init"]
    descriptions = [
        "初始化入口",
        "用于初始化系统模块",
    ]
    sub_commands = []

    # flags
    class flags:
        http_port = FlagInt(flags=["-p", "--http-port"], default=8080)
        http_host = FlagStr(flags=["-h", "--http-host"], default="0.0.0.0")
        log_level = FlagStr(flags=["-l", "--log-level"], default="info")
        enable_debug = FlagBool(flags=["--debug"], default=False)
        enable_tls = FlagBool(flags=["--tls"], default=True)

    def run(self):
        print(self.flags.http_port.value() + 1)
        print(self.flags.http_host.value() + "!!!!")
        print("hello, cc~")


cmd = InitCommand()
cmd.run()
