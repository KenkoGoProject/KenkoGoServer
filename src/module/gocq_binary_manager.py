import tarfile
import zipfile
from pathlib import Path

import requests

from common.logger_ex import LoggerEx, LogLevel
from common.release import Asset, Release
from common.singleton_type import SingletonType
from common.utils import (dict_to_object, download_file, get_os_type,
                          os_type_to_asset_finder)
from exception import ReleaseNotFoundError
from module.global_dict import Global


class GocqBinaryManager(metaclass=SingletonType):
    """go-cqhttp 二进制文件处理"""

    def __init__(self):
        self.log = LoggerEx(self.__class__.__name__)
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.remote_versions: list[Release] = []

    def get_remote_release(self, use_cache: bool = True) -> list[Release]:
        """获取远端发行版列表

        :param use_cache: 是否使用缓存
        :return: 远端发行版列表
        """
        if use_cache and self.remote_versions:
            self.log.debug('Get remote version from cache.')
            return self.remote_versions
        self.log.debug('Getting remote version...')
        release_url = 'https://api.github.com/repos/Mrs4s/go-cqhttp/releases'
        try:
            release_content: list[dict] = requests.get(release_url).json()
        except Exception as e:
            self.log.error(f'Get remote version failed: {e}')
            return []
        result: list[Release] = []
        for item in release_content:
            obj: Release = dict_to_object(item, Release)
            result.append(obj)
            assets: dict = obj.assets.copy()
            obj.assets = [dict_to_object(asset, Asset) for asset in assets]
        self.remote_versions = result
        return result

    def download_remote_version(self, tag_name: str = None) -> bool:
        """下载远端发行版

        :param tag_name: 标签名
        """
        if Global().instance_manager.instance_started:
            self.log.error('Cannot download remote version while go-cqhttp is running.')
            return False

        remote_versions = self.get_remote_release()
        if not tag_name:
            tag_name = remote_versions[0].tag_name
        self.log.debug(f'Looking for remote version: {tag_name}')

        finder = os_type_to_asset_finder(get_os_type())
        for release in remote_versions:
            if release.tag_name == tag_name:
                for asset in release.assets:
                    if finder.search(asset.name):
                        self.log.debug(f'Found {asset.name}')
                        self.log.debug(f'Url {asset.browser_download_url}')
                        file_path = Path(Global().download_dir, 'gocq.compression')
                        try:
                            download_url = asset.browser_download_url
                            proxy = Global().user_config.github_proxy
                            if proxy == 'ghproxy.com':
                                download_url = f'https://ghproxy.com/{download_url}'
                            download_file(download_url, str(file_path))
                        except Exception as e:
                            self.log.error(f'Download failed: {e}')
                            return False
                        try:
                            self.decompress_gocq(str(file_path))
                        except Exception as e:
                            self.log.error(f'Decompress failed: {e}')
                            return False
                        return True
        raise ReleaseNotFoundError(f'Release {tag_name} not found.')

    def decompress_gocq(self, file_path: str) -> None:
        """解压gocq.compression文件

        :param file_path: gocq.compression文件路径
        """

        if Global().instance_manager.instance_started:
            self.log.error('Cannot decompress gocq.compression while go-cqhttp is running.')
            return

        self.log.debug('Decompressing gocq.compression...')
        Global().gocq_dir.mkdir(parents=True, exist_ok=True)
        if Global().is_windows:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                if Global().gocq_binary_name not in zip_ref.namelist():
                    raise FileNotFoundError(f'{Global().gocq_binary_name} not found.')
                zip_ref.extract(Global().gocq_binary_name, Global().gocq_dir)
        else:
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                if Global().gocq_binary_name not in tar_ref.getnames():
                    raise FileNotFoundError(f'{Global().gocq_binary_name} not found.')
                tar_ref.extract(Global().gocq_binary_name, Global().gocq_dir)

    # TODO: 删除等操作
