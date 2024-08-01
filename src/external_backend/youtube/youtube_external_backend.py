from re import match
from typing import List
from external_backend.base import ExternalBackend
from pytubefix import Playlist


class YoutubeExternalBackend(ExternalBackend):
    def is_valid_url(url: str) -> bool:
        """
        Validate a URL to ensure it is a valid YouTube URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is a valid YouTube URL, False otherwise.
        """
        # Use a regex to check if the URL is a valid YouTube URL
        return (
            match(
                r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+",
                url,
            )
            is not None
        )

    def is_in_a_playlist(url: str) -> bool:
        """
        Check if the video is in a playlist.

        Args:
            url (str): The URL of the video.

        Returns:
            bool: True if the video at the URL is inside of a playlist, False otherwise.
        """
        return "list" in url

    def get_playlist_youtube_urls(url: str) -> List[str]:
        yt_playlist = Playlist(url, use_oauth=True, allow_oauth_cache=True)
        return [video.watch_url for video in yt_playlist.videos]

    def get_track_youtube_url(self, url: str) -> str:
        return url
