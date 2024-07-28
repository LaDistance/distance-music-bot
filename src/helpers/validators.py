from helpers.logger import logger
from re import match


def is_valid_youtube_url(url: str) -> bool:
    """
    Validate a URL to ensure it is a valid YouTube URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is a valid YouTube URL, False otherwise.
    """
    # Use a regex to check if the URL is a valid YouTube URL
    return (
        match(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+", url)
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
    logger.info("I'm in a playlist")
    return ("list" in url)