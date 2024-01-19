class NoMorePinsException(Exception):
    def __init__(self) -> None:
        super().__init__(f"No more pins in scheduler left")