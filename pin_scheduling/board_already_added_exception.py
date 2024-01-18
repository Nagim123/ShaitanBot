class BoardAlreadyAddedException(Exception):
    def __init__(self, board_owner: str, board_name: str) -> None:
        super().__init__(f"{board_name} of user {board_owner} was already added")
        self.__board_owner = board_owner
        self.__board_name = board_name
    
    def get_user_format_error(self) -> str:
        return f"Доска {self.__board_name} пользователя {self.__board_owner} уже добавлена"