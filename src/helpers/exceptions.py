class NoSongFound(Exception):
    def __init__(self, query):
        self.query = query
        super().__init__(f"No song found for query '{query}'")
