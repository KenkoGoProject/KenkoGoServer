from typing import List


class Asset:
    id: int = 0
    name: str = ''
    content_type: str = ''
    size: int = 0
    state: str = ''
    browser_download_url: str = ''


class Release:
    id: int = 0
    tag_name: str = ''
    name: str = ''
    published_at: str = ''
    body: str = ''
    assets: List[Asset] = []
