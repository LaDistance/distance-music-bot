from helpers.login import login_to_spotify
from helpers.search import search_for_songs_in_playlist


if __name__ == "__main__":
    spotify = login_to_spotify()
    playlist_id = "2m7ZjGgqKGY9t9FxRbbhVh"
    playlist_tracks = spotify.playlist_tracks(playlist_id)

    playlist_track_names = [
        f"{track['track']['artists'][0]['name']} - {track['track']['name']}"
        for track in playlist_tracks["items"]
    ]
    print(playlist_track_names[:5])
    youtube_urls = search_for_songs_in_playlist(playlist_track_names[:5])
    print(youtube_urls)
