class WrongSchedulingTimeException(Exception):
    def __init__(self) -> None:
        super().__init__(f"This channel is not ready for daily pin!")