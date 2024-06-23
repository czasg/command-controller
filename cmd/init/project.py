# coding: utf-8
import cc

class FlagValueTransform:

    def __getattribute__(self, item):
        if isinstance(item, (cc.FlagStr, cc.FlagBool)):
            return item.value

def to():
    pass

class ProjectCommand(cc.Command):

    class flags:
        path = cc.FlagInt(flags=["-p", "--path"], default=".", description="项目路径")
        name = cc.FlagStr(flags=["-n", "--name"], default="demo")

    def entrypoints(self) -> [str]:
        return ['proj', 'project']

    def run(self):
        print(self.flags.path)
        print(f"cron sever start path={self.flags.path.value} name={self.flags.name.value}")
        # self.flags.path += 1
        value  = 100
        print(value + self.flags.path.value)

cmd = ProjectCommand()
cmd.help()