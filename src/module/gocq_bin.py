import tarfile
import zipfile
from pathlib import Path

import requests

from assets.os_type import OSType
from assets.release import Asset, Release
from module.exception_ex import ReleaseNotFoundError
from module.global_dict import Global
from module.logger_ex import LoggerEx, LogLevel
from module.singleton_type import SingletonType
from module.utils import (dict_to_object, download_file, get_os_type,
                          os_type_to_asset_finder)


class GocqBin(metaclass=SingletonType):
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
        # TODO: review
        if use_cache and self.remote_versions:
            self.log.debug('Get remote version from cache.')
            return self.remote_versions
        self.log.debug('Getting remote version...')
        release_url = 'https://api.github.com/repos/Mrs4s/go-cqhttp/releases'
        release_content: list[dict] = requests.get(release_url).json()
        result: list[Release] = []
        for item in release_content:
            obj: Release = dict_to_object(item, Release)
            result.append(obj)
            assets: dict = obj.assets.copy()
            obj.assets = [dict_to_object(asset, Asset) for asset in assets]
        self.remote_versions = result
        return result

    def download_remote_version(self, tag_name: str = None) -> None:
        """下载远端发行版

        :param tag_name: 标签名
        """
        # TODO: review
        self.get_remote_release()
        if not tag_name:
            tag_name = self.remote_versions[0].tag_name
        self.log.debug(f'Looking for remote version: {tag_name}')

        for release in self.remote_versions:
            if release.tag_name == tag_name:
                os_type = get_os_type()
                finder = os_type_to_asset_finder(os_type)
                for asset in release.assets:
                    if finder.search(asset.name):
                        self.log.debug(f'Found {asset.name}')
                        self.log.debug(f'Url {asset.browser_download_url}')
                        file_path = Path(Global().download_dir) / 'gocq.compression'
                        download_file(asset.browser_download_url, str(file_path))
                        self.decompress_gocq(str(file_path))
                        return
        raise ReleaseNotFoundError(f'Release {tag_name} not found.')

    def decompress_gocq(self, file_path: str) -> None:
        """解压gocq.compression文件

        :param file_path: gocq.compression文件路径
        """
        # TODO: review
        self.log.debug('Decompressing gocq.compression...')
        Global().gocq_asset_dir.mkdir(parents=True, exist_ok=True)
        os_type = get_os_type()
        if os_type in [OSType.WINDOWS_AMD64, OSType.WINDOWS_I386]:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                if Global().gocq_bin_name not in zip_ref.namelist():
                    raise FileNotFoundError(f'{Global().gocq_bin_name} not found.')
                zip_ref.extract(Global().gocq_bin_name, Global().gocq_asset_dir)
        elif os_type in [OSType.LINUX_AMD64, OSType.LINUX_I386]:
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                if Global().gocq_bin_name not in tar_ref.getnames():
                    raise FileNotFoundError(f'{Global().gocq_bin_name} not found.')
                tar_ref.extract(Global().gocq_bin_name, Global().gocq_asset_dir)

    # TODO: 删除等操作
