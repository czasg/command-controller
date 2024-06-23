# # coding: utf-8
# import sys
#
# from cc import *
#
#
# class AppCommand(Command):
#     # command
#     alias = ["app"]
#     descriptions = [
#         "初始化入口",
#         "用于初始化系统模块",
#     ]
#     sub_commands = []
#
#     # flags
#     class flags:
#         http_port = FlagInt(flags=["-p", "--http-port"], default=8080)
#         http_host = FlagStr(flags=["-h", "--http-host"], default="0.0.0.0")
#         log_level = FlagStr(flags=["-l", "--log-level"], default="info")
#         enable_debug = FlagBool(flags=["--debug"], default=False)
#         enable_tls = FlagBool(flags=["--tls"], default=True)
#
#     def run(self):
#         print(self.flags.http_port.value() + 1)
#         print(self.flags.http_host.value() + "!!!!")
#         print("hello, cc~")
#
#
# class ProjectCommand(Command):
#     # command
#     alias = ["proj", "project"]
#     descriptions = [
#         "初始化入口",
#         "用于初始化系统模块",
#     ]
#     sub_commands = []
#
#     # flags
#     class flags:
#         http_port = FlagInt(flags=["-p", "--http-port"], default=8080)
#         http_host = FlagStr(flags=["-h", "--http-host"], default="0.0.0.0")
#         log_level = FlagStr(flags=["-l", "--log-level"], default="info")
#         enable_debug = FlagBool(flags=["--debug"], default=False)
#         enable_tls = FlagBool(flags=["--tls"], default=True)
#
#     def run(self):
#         print(self.flags.http_port.value() + 1)
#         print(self.flags.http_host.value() + "!!!!")
#         print("hello, cc~")
#
#
# class InitCommand(Command):
#     # command
#     alias = ["init"]
#     descriptions = [
#         "初始化入口",
#         "用于初始化系统模块",
#     ]
#     sub_commands = [
#         ProjectCommand,
#         AppCommand,
#     ]
#
#     # flags
#     class flags:
#         http_port = FlagInt(flags=["-p", "--http-port"], default=8080)
#         http_host = FlagStr(flags=["-h", "--http-host"], default="0.0.0.0")
#         log_level = FlagStr(flags=["-l", "--log-level"], default="info")
#         enable_debug = FlagBool(flags=["--debug"], default=False)
#         enable_tls = FlagBool(flags=["--tls"], default=True)
#
#     def run(self):
#         print(self.flags.http_port.value() + 1)
#         print(self.flags.http_host.value() + "!!!!")
#         print("hello, cc~")
#
#
# class ServerCommand:
#     # command
#     alias = ["server"]
#     descriptions = [
#         "服务端入口",
#         "服务端入口",
#     ]
#     sub_commands = []
#
#     # flags
#     class flags:
#         http_port = FlagInt(flags=["-p", "--http-port"], default=8080)
#         http_host = FlagStr(flags=["-h", "--http-host"], default="0.0.0.0")
#         log_level = FlagStr(flags=["-l", "--log-level"], default="info")
#         enable_debug = FlagBool(flags=["--debug"], default=False)
#         enable_tls = FlagBool(flags=["--tls"], default=True)
#
#     def run(self):
#         print(self.flags.http_port.value() + 1)
#         print(self.flags.http_host.value() + "!!!!")
#         print("hello, cc~")
#
#
# class Manager:
#
#     def __init__(self, *commands):
#         pass
#
#     def exec(self, argv):
#         pass
#
#
# root = Command()
# root.add(
#     InitCommand(),
#     ServerCommand(),
# )

arr = [1]
for i in arr[0:]:
    print(i)
