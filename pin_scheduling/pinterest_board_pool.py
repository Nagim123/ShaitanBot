import os
from config import Config
from pinterest_board_parser.pinterest_board import PinterestBoard

class PinterestBoardPool:
    def __init__(self) -> None:
        self.__board_cache_folder_path = Config.data()["PINTEREST_BOARD_CACHE_FOLDER"]
        self.__board_pool: dict[str, tuple[PinterestBoard, int]] = dict()
        self.__load_from_file()

    def link_board(self, board_owner: str, board_name: str) -> PinterestBoard:
        board_unique_name = f"{board_owner} {board_name}"
        
        used_count = 0
        if board_unique_name in self.__board_pool:
            board, used_count = self.__board_pool[board_unique_name]
        else:
            board = PinterestBoard(board_owner, board_name, f"{self.__board_cache_folder_path}/{board_unique_name}")
        
        self.__board_pool[board_unique_name] = (board, used_count + 1)
        return board

    def unlink_board(self, board_owner: str, board_name: str) -> None:
        board_unique_name = f"{board_owner} {board_name}"

        if not board_unique_name in self.__board_pool:
            raise Exception(f"Board with name {board_name} and author {board_owner} does not stored in the pool")

        board, used_count = self.__board_pool[board_unique_name]
        if used_count > 1:
            self.__board_pool[board_unique_name] = (board, used_count - 1)
        else:
            os.remove(f"{self.__board_cache_folder_path}/{board_unique_name}")
            del self.__board_pool[board_unique_name]
    
    def __load_from_file(self) -> None:
        for board_unique_name in os.listdir(self.__board_cache_folder_path):
            board_path = self.__board_cache_folder_path + '/' + board_unique_name
            if os.path.isfile(board_path):
                board_owner, board_name = board_unique_name.split(" ")
                self.__board_pool[board_unique_name] = (PinterestBoard(board_owner, board_name, board_path), 0)