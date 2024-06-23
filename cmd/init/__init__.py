# coding: utf-8
import cc

from .ddl import cmd as ddlCmd
from .project import cmd as ProjectCmd


class InitCommand(cc.Command):

    def run(self):
        print("cron sever start")


cmd = InitCommand()
cmd.add(
    ddlCmd,
    ProjectCmd
)
