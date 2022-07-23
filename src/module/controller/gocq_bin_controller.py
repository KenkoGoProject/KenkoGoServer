import requests
from fastapi import APIRouter

from module.global_dict import Global
from module.http_result import HttpResult
from module.logger_ex import LoggerEx, LogLevel


class GocqBinController(APIRouter):
    remote_versions: list[dict] = []

    def __init__(self, *args, **kwargs):
        super().__init__(prefix='/gocqbin', *args, **kwargs)
        self.log = LoggerEx('GocqBinController')
        if Global().debug_mode:
            self.log.set_level(LogLevel.DEBUG)
        self.log.debug('GocqBinController Initializing...')

        self.add_api_route('/remoteversion', self.get_remote_version, methods=['GET'])

    async def get_remote_version(self, use_cache: bool = True):
        if use_cache and self.remote_versions:
            self.log.debug('Get remote version from cache.')
            return HttpResult.success(self.remote_versions)
        self.log.debug('Getting remote version...')
        release_url = 'https://api.github.com/repos/Mrs4s/go-cqhttp/releases'
        release_content = requests.get(release_url).json()
        self.remote_versions = release_content
        return HttpResult.success(release_content)

    async def download_remote_version(self, version: str):
        self.log.debug(f'Downloading remote version: {version}')
        release_url = f'https://api.github.com/repos/Mrs4s/go-cqhttp/releases/tags/{version}'
        release_content = requests.get(release_url).json()
        download_url = release_content['assets'][0]['browser_download_url']
        return requests.get(download_url).content
