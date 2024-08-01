from pytubefix import YouTube
from helpers.root import get_project_root

def login_to_youtube() -> None:
    yt = YouTube(
        "https://www.youtube.com/watch?v=48AEpQkM8nU",
        use_oauth=True,
        allow_oauth_cache=True,
        token_file=f"{get_project_root()}/tmp/youtube_token.json",
    )
    # Try to access the video title to trigger OAuth login
    title = yt.title
