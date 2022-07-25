import argparse
import signal
import sys

from rich.traceback import install as install_rich_traceback

from module.console import Console
from module.exception_ex import AnyException
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.user_config import UserConfig


class Main:
    # 信号响应处理器
    def signal_handler(self, sign, _):
        if sign in (signal.SIGINT, signal.SIGTERM):
            self.log.debug(f'Received signal {sign}, Application exits.')
            Global().time_to_exit = True

    # 命令处理器
    def command_handler(self, _command):
        if _command == '/help':
            help_text = """/help: Show this help message
/exit: Exit Application"""
            Global().console.print(help_text)
        elif _command == '/exit':
            Global().time_to_exit = True
        else:
            self.log.error('Invalid Command')

    def __init__(self):
        Global().console = Console()  # 初始化控制台对象
        install_rich_traceback(console=Global().console, show_locals=True)  # 捕获未处理的异常

        # 命令行参数解析
        parser = argparse.ArgumentParser(
            description=f'{Global().app_name} - A Controller of go-cqhttp',  # 应用程序的描述
            add_help=False,  # 不输出自动生成的说明
            exit_on_error=False,  # 发生错误时不退出
        )
        parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
        parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
        parser.add_argument('-c', '--config', help='Config file path', default='config.yaml')
        args_known, args_unknown = parser.parse_known_args()

        if args_known.help:
            parser.print_help()
            sys.exit(0)

        debug_mode = args_known.debug  # 开启调试模式
        Global().debug_mode = debug_mode

        # 创建日志打印器
        self.log: LoggerEx = LoggerEx(self.__class__.__name__)
        self.log.set_level(LogLevel.DEBUG if debug_mode else LogLevel.INFO)

        # 加载用户配置
        self.log.debug('Loading Config...')
        Global().user_config = UserConfig(args_known.config)

        # 设置信号响应
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # 启动程序
        self.run_forever()

    def run_forever(self):
        self.log.debug(f'{Global().app_name} Starting...')
        app = None

        try:
            # 启动应用
            from kenko_go import KenkoGo
            app = KenkoGo()
            app.start()
        except AnyException:
            Global().console.print_exception(show_locals=True)
            Global().time_to_exit = True
            self.log.critical('Critical Error, Application exits abnormally.')  # 发生致命错误，应用异常退出

        while not Global().time_to_exit:
            try:
                command = Global().console.input('> ')  # 获取用户输入
            except (UnicodeDecodeError, EOFError, KeyboardInterrupt):
                if Global().time_to_exit:
                    break  # 退出
                else:
                    self.log.error('Invalid Command')  # 输入的命令无效
            else:
                Global().command = command
                self.command_handler(command)

        # 退出程序
        from kenko_go import KenkoGo
        if isinstance(app, KenkoGo):
            app.stop()
        self.log.debug(f'{Global().app_name} Exits.')
        sys.exit(Global().exit_code)


if __name__ == '__main__':
    # 让PyCharm调试输出的信息换行
    if sys.gettrace() is not None:
        print('Debug Mode')

    # 启动程序
    sys.exit(Main())
