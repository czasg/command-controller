# coding: utf-8
import cc

from cmd.cron import cmd as CronCmd
from cmd.init import cmd as InitCmd
from cmd.server import cmd as ServerCmd


def start():
    cmd = cc.NewCommand()
    cmd.add(
        CronCmd,
        InitCmd,
        ServerCmd
    )
    cc.Execute(cmd)

    import argparse

