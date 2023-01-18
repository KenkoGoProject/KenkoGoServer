import re
import subprocess
import time
from typing import Union

from assets.server_event import ServerEvent
from module.exception_ex import DownloadError
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType
from module.thread_ex import ThreadEx
from module.utils import decode_qrcode, print_qrcode


class InstanceManager(metaclass=SingletonType):
    """go-cqhttp 实例控制"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.proc_log = LoggerEx('Process')
        if Global().debug_mode:
            self.proc_log.set_level(LogLevel.DEBUG)

        self.instance_started = False  # 实例是否已启动
        self.ready_to_start = False  # 实例是否准备好启动

        self.process: Union[subprocess.Popen, None] = None  # go-cqhttp 实例进程
        self.thread_read_output: Union[ThreadEx, None] = None  # 控制台输出检查线程
        self.websocket_manager = Global().websocket_manager

    def check(self) -> None:
        """检查是否初始化"""

        # 检查 go-cqhttp 是否存在
        if not Global().gocq_path.exists():
            self.log.warning('go-cqhttp not found, try to download it.')
            try:
                ok = Global().gocq_binary_manager.download_remote_version()
                if not ok:
                    raise DownloadError('Download failed.')
            except Exception as e:
                self.log.error(e)
                self.ready_to_start = False
                return

        # 检查配置文件
        Global().gocq_config.refresh()
        self.ready_to_start = True

    def start(self) -> bool:
        if self.instance_started:
            self.log.warning('Instance already started')
            return False
        if not self.ready_to_start:
            self.check()
        if not self.ready_to_start:
            self.log.warning('Instance not ready to start')
            return False
        self.log.debug('Starting go-cqhttp...')
        if Global().is_windows:
            exec_path = Global().gocq_path
        else:
            exec_path = f'./{Global().gocq_binary_name}'
        self.process = subprocess.Popen(
            args=[exec_path, '-faststart'],
            cwd=Global().gocq_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
        )
        self.instance_started = True
        self.thread_read_output = ThreadEx(target=self._read_output)
        self.thread_read_output.start()
        return True

    def stop(self) -> bool:
        if not self.instance_started:
            self.log.warning('Instance not started')
            return False
        self.log.debug('Stopping go-cqhttp...')
        self.instance_started = False
        self.ready_to_start = False
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(2)
            if self.process.poll() is None:
                self.log.error('go-cqhttp is still running, force to kill it.')
                self.process.kill()
        if self.thread_read_output:
            ...
        self.process = None
        self.thread_read_output = None
        return True

    def restart(self):
        self.stop()
        time.sleep(0.5)
        self.start()

    def _read_output(self) -> None:
        """控制台输出检查线程"""
        while self.process and self.process.poll() is None:
            output_list = self.process.stdout.readlines(1)
            if not output_list:
                continue
            text_output: str = output_list[0]
            text_output = text_output.strip()

            # 删除颜色标签
            color_regex = re.compile(r'\x1b\[\d+(;\d+)?m')
            match_result = re.match(color_regex, text_output)
            if not match_result:
                self.proc_log.debug(text_output)
                continue
            text_output = re.sub(color_regex, '', text_output).strip()

            # 删除日期与日志等级
            match_result = re.match(r'\[\d+-\d+-\d+ \d+:\d+:\d+] \[[A-Z]+\]: ', text_output)
            if not match_result:
                self.proc_log.debug(text_output)
                continue
            if match_result.end() == len(text_output):
                self.proc_log.debug(text_output)
                continue
            text_output = text_output[match_result.end():].strip()

            if not text_output:
                continue

            self.proc_log.debug(text_output)
            if self.handle_output(text_output):
                break
        self.instance_started = False

    def handle_output(self, text_output: str) -> bool:
        """处理控制台输出

        :param text_output: 控制台输出
        :return: 是否退出线程
        """
        if text_output.startswith('请使用手机QQ扫描二维码 (qrcode.png)'):
            self.on_need_scan()
        elif text_output.startswith('上报 Event 数据'):
            ...
        elif text_output.startswith('开始尝试登录并同步消息'):
            ...
        elif text_output.startswith('检查更新完成. 当前已运行最新版本'):
            ...
        elif text_output.startswith('资源初始化完成, 开始处理信息'):
            ...
        elif text_output.startswith('当前版本:'):
            ...
        elif text_output.startswith('使用协议: '):
            ...
        elif text_output.startswith('将使用 device.json 内的设备信息运行Bot.'):
            ...
        elif text_output.startswith('账号密码未配置, 将使用二维码登录'):
            ...
        elif text_output.startswith('扫码成功, 请在手机端确认登录.'):
            self.log.info('Scan success. Please confirm in your phone.')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('scan_success'))
        elif text_output.startswith('恢复会话失败: Packet timed out , 尝试使用正常流程登录'):
            ...
        elif text_output.startswith('Bot 账号在客户端'):
            ...
        elif text_output.startswith('Protocol -> '):
            text_output = text_output.removeprefix('Protocol -> ')
            # Protocol -> parse incoming packet error: return code unsuccessful: -10001
            if text_output.startswith('connect to server'):
                return False
            elif text_output.startswith('unexpected disconnect: '):
                self.log.warning(f'预期外的断线: {text_output.removeprefix("unexpected disconnect: ")}')
            elif text_output.startswith('register client failed: Packet timed out'):
                self.log.warning('注册客户端失败: 数据包超时')
            elif text_output.startswith('connect server error: dial tcp error: '):
                self.log.warning('服务器连接失败')
            elif text_output.startswith('resolve long message server error'):
                self.log.warning('长消息服务器延迟测试失败')
            elif text_output.startswith('test long message server response latency error'):
                self.log.warning('长消息服务器响应延迟测试失败')
            elif text_output.startswith('device lock is disable.'):
                self.log.warning('设备锁未启用, http api可能失败')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event(f'protocol: {text_output}'))
        elif text_output.startswith('Bot已离线: '):
            self.log.warning(text_output)
        elif text_output.startswith('扫码登录无法恢复会话'):
            self.log.warning('快速重连失败，扫码登录无法恢复会话，go-cqhttp将重启')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('fail_reconnect'))
            self.restart()
            return True
        elif text_output.startswith('登录时发生致命错误: '):
            text_output = text_output.removeprefix('登录时发生致命错误: ')
            if text_output.startswith('fetch qrcode error: Packet timed out'):
                self.log.warning('二维码获取失败，等待重新生成二维码')
            elif text_output.startswith('not found error correction level and mask'):
                ...
            else:
                self.log.warning(text_output)
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event(f'login_error: {text_output}'))
            self.restart()
            return True
        elif text_output.startswith('扫码被用户取消.'):
            self.log.warning('二维码登录被取消')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('scan_cancel'))
            self.restart()
            return True
        elif text_output.startswith('二维码过期'):
            self.log.warning('二维码已过期，等待重新生成二维码')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('qrcode_expired'))
            self.restart()
            return True
        elif text_output.startswith('登录成功 欢迎使用:'):
            self.log.info('登录成功，正在等待消息上报')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('login_success'))
        elif text_output.startswith('检查更新失败: '):
            text_output = text_output.removeprefix('检查更新失败: ')
            # Get "https://api.github.com/repos/Mrs4s/go-cqhttp/releases/latest"
            # : dial tcp: lookup api.github.com: no such host
            self.log.warning(f'检查更新失败，请检查github访问是否通畅。 {text_output}')
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event(f'check_update_fail: {text_output}'))
        elif text_output.startswith('快速重连失败'):
            text_output = text_output.removeprefix('快速重连失败').strip()
            if text_output.startswith(', 扫码登录无法恢复会话.'):
                self.log.warning('重连失败，go-cqhttp将重启')
                self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('fail_reconnect'))
                self.restart()
                return True
        elif text_output.startswith('群消息发送失败: '):
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('failed to send group message'))
            self.log.warning(text_output)
        elif text_output.startswith('频道消息发送失败: '):
            self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('failed to send channel message'))
            self.log.warning(text_output)

    def on_need_scan(self) -> None:
        self.log.info(f'等待扫描二维码 http://{Global().host_with_port}/instance/qrcode')
        self.websocket_manager.broadcast_sync(ServerEvent.gocq_event('need_scan'))
        try:
            with Global().qrcode_path.open('rb') as f:
                qrcode = f.read()
            code_url = decode_qrcode(qrcode)
            print_qrcode(code_url)
        except Exception as e:
            self.log.exception(e)
