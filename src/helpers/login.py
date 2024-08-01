from pytubefix import YouTube

def login_to_youtube() -> None:
    yt = YouTube(
        "https://www.youtube.com/watch?v=48AEpQkM8nU",
        use_oauth=True,
        allow_oauth_cache=True,
    )
    # Try to access the video title to trigger OAuth login
    title = yt.title
