import re
import shutil
import subprocess
import threading
from typing import Union

from module.global_dict import Global
from module.gocq_config import GocqConfig
from module.logger_ex import LoggerEx, LogLevel


class GocqInstance:  # TODO: 此处应使用单例模式
    """go-cqhttp 实例控制"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.proc_log = LoggerEx('Process')
        if Global().debug_mode:
            self.proc_log.set_level(LogLevel.DEBUG)

        Global().gocq_config = GocqConfig()
        self.process: Union[subprocess.Popen, None] = None  # go-cqhttp 实例进程
        self.thread_read_output: Union[threading.Thread, None] = None  # 控制台输出检查线程

    def check(self) -> None:
        """检查是否初始化"""
        # TODO: 检查是否初始化
        Global().gocq_config.create_default_config()
        shutil.copyfile(Global().gocq_bin_path, Global().gocq_path)

    def start(self) -> None:
        # TODO: 检查是否初始化与已启动
        self.log.debug('Starting gocq...')
        self.process = subprocess.Popen(
            args=f'{Global().gocq_path} -faststart',
            cwd=Global().gocq_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )
        self.thread_read_output = threading.Thread(target=self._read_output)
        self.thread_read_output.start()

    def stop(self) -> None:
        # TODO: 检查是否初始化与已启动
        self.log.debug('Stopping gocq...')
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(2)
            if self.process.poll() is None:
                self.log.error('gocq is still running, force to kill it.')
                self.process.kill()
        if self.thread_read_output:
            self.thread_read_output.join()
        self.process = None
        self.thread_read_output = None

    def _read_output(self) -> None:
        """控制台输出检查线程"""
        while self.process.poll() is None:
            output_list = self.process.stdout.readlines(1)
            if not output_list:
                continue
            text_output: str = output_list[0]
            text_output = text_output.strip()

            # 删除颜色标签
            color_regex = re.compile(r'\x1b\[\d+(;\d+)?m')
            match_result = re.match(color_regex, text_output)
            if not match_result:
                continue
            text_output = re.sub(color_regex, '', text_output).strip()

            # 删除日期与日志等级
            match_result = re.match(r'\[\d+-\d+-\d+ \d+:\d+:\d+] \[[A-Z]+\]: ', text_output)
            if not match_result:
                continue
            if match_result.end() == len(text_output):
                continue
            text_output = text_output[match_result.end():].strip()

            if not text_output:
                continue

            self.proc_log.debug(text_output)
            self.handle_output(text_output)

    def handle_output(self, text_output: str):
        """处理控制台输出"""
        # TODO: 补充情况
        if text_output.startswith('请使用手机QQ扫描二维码 (qrcode.png)'):
            self.log.info(f'等待扫描二维码 http://{Global().host_with_port}/instance/qrcode')
