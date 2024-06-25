# coding: utf-8
import cc


class CronCommand(cc.Command):
    class flags:
        cron = cc.FlagStr(flags=["-c"], default="* * * * *")

    def run(self):
        print("cron sever start", self.flags.cron)


cmd = CronCommand()
