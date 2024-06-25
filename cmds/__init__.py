# coding: utf-8
import cc

from cmds.cron import cmd as CronCmd
from cmds.init import cmd as InitCmd
from cmds.server import cmd as ServerCmd


def start():
    cmd = cc.NewCommand()
    cmd.add(
        CronCmd,
        InitCmd,
        ServerCmd
    )
    cc.Execute(cmd)
