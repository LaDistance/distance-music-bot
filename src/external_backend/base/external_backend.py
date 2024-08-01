from abc import ABC, abstractmethod
from typing import List


class ExternalBackend(ABC):
    @abstractmethod
    def is_valid_url(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_in_a_playlist(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_playlist_youtube_urls(self, url: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_track_youtube_url(self, url: str) -> str:
        raise NotImplementedError
