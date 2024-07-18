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
