# coding: utf-8
import cc


class DdlCommand(cc.Command):
    class flags:
        file = cc.FlagStr(flags=["-f", "--file"], default="ddl.sql")

    def run(self):
        print("cron sever start")


cmd = DdlCommand()
