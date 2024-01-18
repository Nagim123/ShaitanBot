import os
from pinterest_board_parser.pinterest_board import PinterestBoard
from pin_scheduling.pinterest_board_scheduler import PinterestBoardScheduler
from pin_scheduling.pinterest_board_pool import PinterestBoardPool
from pin_scheduling.board_not_found_exception import BoardNotFoundException
from pin_scheduling.board_already_added_exception import BoardAlreadyAddedException
from config import Config

class PinteresetChannelScheduler:
    def __init__(self, channel_id: int, board_pool: PinterestBoardPool) -> None:
        self.channel_cache_folder_path = Config.data()["PINTEREST_BOARD_SCHEDULE_CACHE_FOLDER"] + '/' + str(channel_id)
        self.board_pool = board_pool
        self.__schedulers: dict[str, PinterestBoardScheduler] = dict()
        if os.path.exists(self.channel_cache_folder_path):
            self.__load_from_file()
    
    def add_pin_board(self, board_owner: str, board_name: str, board: PinterestBoard) -> None:
        board_unique_name = f"{board_owner} {board_name}"

        if board_unique_name in self.__schedulers:
            raise BoardAlreadyAddedException(board_owner, board_name)
        
        if not os.path.exists(self.channel_cache_folder_path):
            os.mkdir(self.channel_cache_folder_path)

        self.__schedulers[board_unique_name] = PinterestBoardScheduler(board, f"{self.channel_cache_folder_path}/{board_unique_name}")

    def remove_pin_board(self, board_owner: str, board_name: str) -> None:
        board_unique_name = f"{board_owner} {board_name}"

        if not board_unique_name in self.__schedulers:
            raise BoardNotFoundException(board_owner, board_name)
        
        del self.__schedulers[board_unique_name]
        os.remove(f"{self.channel_cache_folder_path}/{board_unique_name}")

        if len(self.__schedulers) == 0:
            os.rmdir(self.channel_cache_folder_path)

    def __load_from_file(self) -> None:
        for board_unique_name in os.listdir(self.channel_cache_folder_path):
            scheduler_path = self.channel_cache_folder_path + '/' + board_unique_name
            if os.path.isfile(scheduler_path):
                board_owner, board_name = board_unique_name.split(' ')
                scheduler = PinterestBoardScheduler(self.board_pool.link_board(board_owner, board_name), scheduler_path)
                self.__schedulers[board_unique_name] = scheduler