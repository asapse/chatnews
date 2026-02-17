class Chunk:
    def __init__(self, chunk_size: int = 500) -> None:
        self._chunk_size: int = chunk_size
