from re import match
from typing import List
from external_backend.base import ExternalBackend
from pytubefix import Search
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.exceptions import NoSongFound


class SpotifyExternalBackend(ExternalBackend):
    def __init__(self):
        self.spotify = self._login()

    def _login(self):
        return Spotify(auth_manager=SpotifyClientCredentials())

    def _search_for_track(self, track_name: str) -> str:
        """
        Search for a track on YouTube and return the first result.

        Args:
            track_name (str): The name of the track to search for.

        Returns:
            str: The URL of the first search result.
        """

        # Search for the track on YouTube
        yt = Search(
            query=track_name,
        )

        # Get the first search result
        if len(yt.videos) == 0:
            raise NoSongFound(track_name)

        return yt.videos[0].watch_url

    def _search_for_songs_in_playlist(
        self, playlist_track_names: List[str]
    ) -> List[str]:
        """
        Search for a list of tracks on YouTube and return the URLs of the search results.

        Args:
            playlist_track_names (List[str]): The list of track names to search for.

        Returns:
            List[str]: The list of URLs of the search results.
        """

        # Search for each track in the playlist
        urls = []
        for track_name in playlist_track_names:
            try:
                url = self._search_for_track(track_name)
                urls.append(url)
            except NoSongFound as e:
                print(e)

        return urls

    def is_valid_url(self, url: str) -> bool:
        """
        Validate a URL to ensure it is a valid Spotify URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is a valid YouTube URL, False otherwise.
        """
        # Use a regex to check if the URL is a valid YouTube URL
        return (
            match(
                r"https?://open\.spotify\.com/(playlist|track|album)/[a-zA-Z0-9]+(\?si=[a-zA-Z0-9]+)?",
                url,
            )
            is not None
        )

    def is_in_a_playlist(self, url: str) -> bool:
        """
        Check if the video is in a playlist.

        Args:
            url (str): The URL of the video.

        Returns:
            bool: True if the video at the URL is inside of a playlist, False otherwise.
        """
        return "playlist" in url

    def get_playlist_youtube_urls(self, url: str) -> List[str]:
        playlist_id = url.split("/")[-1]
        playlist_tracks = self.spotify.playlist_tracks(playlist_id)

        playlist_track_names = [
            f"{track['track']['artists'][0]['name']} - {track['track']['name']}"
            for track in playlist_tracks["items"]
        ]

        return self._search_for_songs_in_playlist(playlist_track_names)

    def get_track_youtube_url(self, url: str) -> str:
        track_id = url.split("/")[-1]
        track = self.spotify.track(track_id)
        track_name = f"{track['artists'][0]['name']} - {track['name']}"

        return self._search_for_track(track_name)
