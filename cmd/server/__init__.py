# coding: utf-8
import cc


class ServerCommand(cc.Command):
    class flags:
        http_port = cc.FlagInt(flags=["-p", "--http-port"], default=8080, require=True)
        http_host = cc.FlagStr(flags=["-h", "--http-host"], default="0.0.0.0")
        log_level = cc.FlagStr(flags=["-l", "--log-level"], default="info")
        enable_debug = cc.FlagBool(flags=["--debug"], default=False)
        enable_tls = cc.FlagBool(flags=["--tls"], default=False, require=True)

    def run(self):
        print("cron sever start")


cmd = ServerCommand()
cmd.help()
