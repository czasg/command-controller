# CommandControl

一个用于替代`argparse`的轻量级命令行控制库.

# 安装
```
pip install command-controller
```

# 快速开始
初始化 `main.py` 文件，内容如下：
```python
import cc

class RunServerCommand(cc.Command):
    class flags:
        host = cc.FlagStr(flags=["--host"], description="server host.", default="0.0.0.0")
        port = cc.FlagInt(flags=["-p", "--port"], description="server port.", default=8080)
        log_level = cc.FlagStr(flags=["--log-level"], description="server log level.", default="info")

    def run(self, *args):
        print("server start")

class RunCronCommand(cc.Command):
    class flags:
        cron = cc.FlagStr(flags=["--cron"], description="cron like '* * * * *'.", require=True)
        log_level = cc.FlagStr(flags=["--log-level"], description="server log level.", default="info")

    def run(self, *args):
        print("cron start")

def main():
    cmd = cc.NewCommand()
    cmd.add(
        RunServerCommand(),
        RunCronCommand(),
    )
    cc.Execute(cmd)

if __name__ == '__main__':
    main()
```

在上述代码中，我们定义了两个指令：

- **RunServerCommand**：启动后端服务。
- **RunCronCommand**：启动后台定时任务。

这时，我们可以分别使用以下指令启动对应的服务：

- `python main.py runserver -p 8000`：启动后端服务，并指定端口为8000.
- `python main.py runcron --cron "0 * * * *"`：启动定时服务，并指定cron参数.

# 命令组合

同样的命令参数，我们可以通过简单的改造，实现命令组合。

```python
import cc

class RunCommand(cc.Command):

    def __init__(self):
        super().__init__()
        self.add(
            ServerCommand(),
            CronCommand(),
        )

class ServerCommand(cc.Command):
    class flags:
        host = cc.FlagStr(flags=["--host"], description="server host.", default="0.0.0.0")
        port = cc.FlagInt(flags=["-p", "--port"], description="server port.", default=8080)
        log_level = cc.FlagStr(flags=["--log-level"], description="server log level.", default="info")

    def run(self, *args):
        print("server start")

class CronCommand(cc.Command):
    class flags:
        cron = cc.FlagStr(flags=["--cron"], description="cron like '* * * * *'.", require=True)
        log_level = cc.FlagStr(flags=["--log-level"], description="server log level.", default="info")

    def run(self, *args):
        print("cron start")

def main():
    cmd = cc.NewCommand()
    cmd.add(
        RunCommand(),
    )
    cc.Execute(cmd)

if __name__ == '__main__':
    main()
```

# Command属性

## run
用于启动指令：
```python
class ServerCommand(cc.Command):

    def run(self, *args):
        print("server start")
```

## flags
用于定义命令行参数，启动后会读取`sys.argv`并填充至对应属性中。然后可以在`run`函数中进行调用，调用方法为`value`：
```python
class ServerCommand(cc.Command):

    class flags:
        host = cc.FlagStr(flags=["--host"], description="server host.", default="0.0.0.0")
        port = cc.FlagInt(flags=["-p", "--port"], description="server port.", default=8080)
        log_level = cc.FlagStr(flags=["--log-level"], description="server log level.", default="info")

    def run(self, *args):
        print("server start: ", self.flags.host.value())
        print("server start: ", self.flags.port.value())
        print("server start: ", self.flags.log_level.value())
```

## entrypoints
用于指定启动指令，默认为小写的类名字，如果类名字以`command`、`cmd`结尾，则程序会帮你去掉。举例：
- 定义类名`HelloCommand`，则`entrypoints`为`hello`
- 定义类名`HelloCmd`，则`entrypoints`为`hello`
- 定义类名`HelloCC`，则`entrypoints`为`hellocc`

我们可以通过自定义`entrypoints`方法实现覆盖，见下：
```python
class ServerCommand(cc.Command):

    def entrypoints() -> str:
        return "server"
```

## usages
用于描述命令使用方法，默认为`[entrypoints] [OPTIONS]`。可以通过自定义`usages`方法实现覆盖，见下：
```python
class ServerCommand(cc.Command):

    def usages() -> str:
        return "run server [OPTIONS]"
```

## descriptions
用于描述命令功能，默认为空。可以通过自定义`descriptions`方法实现覆盖，见下：
```python
class ServerCommand(cc.Command):

    def descriptions() -> str:
        return "启动服务指令"
```
