import os
import datetime
from pinterest_board_parser.pinterest_board import PinterestBoard
from pinterest_board_parser.pinterest_pin import PinterestPin
from pin_scheduling.pinterest_board_scheduler import PinterestBoardScheduler
from pin_scheduling.pinterest_board_pool import PinterestBoardPool
from pin_scheduling.board_not_found_exception import BoardNotFoundException
from pin_scheduling.board_already_added_exception import BoardAlreadyAddedException
from pin_scheduling.wrong_scheduling_time_exception import WrongSchedulingTimeException
from config import Config
from enum import Enum
from random import randint

class SortModes(Enum):
    RANDOM = "random"
    ALHABETIC = "alphabetic"

class PinteresetChannelScheduler:
    def __init__(self, channel_id: int, board_pool: PinterestBoardPool) -> None:
        self.channel_cache_folder_path = Config.data()["PINTEREST_BOARD_SCHEDULE_CACHE_FOLDER"] + '/' + str(channel_id)
        self.__channel_id = channel_id
        self.__board_pool = board_pool
        self.__current_scheduler_index = 0
        self.__accept_time = datetime.time(8, 0, 0)
        self.__sort_mode = SortModes.RANDOM
        self.__schedulers: dict[str, PinterestBoardScheduler] = dict()
        if os.path.exists(self.channel_cache_folder_path):
            self.__load_from_file()
    
    def add_pin_board(self, board_owner: str, board_name: str, board: PinterestBoard) -> None:
        board_unique_name = f"{board_owner} {board_name}"

        if board_unique_name in self.__schedulers:
            raise BoardAlreadyAddedException(board_owner, board_name)
        
        if not os.path.exists(self.channel_cache_folder_path):
            os.mkdir(self.channel_cache_folder_path)
            self.__save_to_file()

        self.__schedulers[board_unique_name] = PinterestBoardScheduler(board, f"{self.channel_cache_folder_path}/{board_unique_name}")

    def remove_pin_board(self, board_owner: str, board_name: str) -> None:
        board_unique_name = f"{board_owner} {board_name}"

        if not board_unique_name in self.__schedulers:
            raise BoardNotFoundException(board_owner, board_name)
        
        del self.__schedulers[board_unique_name]
        os.remove(f"{self.channel_cache_folder_path}/{board_unique_name}")

        if len(self.__schedulers) == 0:
            os.rmdir(self.channel_cache_folder_path)

    def get_scheduled_pin(self) -> PinterestPin:
        if not datetime.datetime.now().hour == self.__accept_time.hour:
            raise WrongSchedulingTimeException()
        print("FFF")
        scheduler_list: list[tuple[str, PinterestBoardScheduler]] = []
        for board_unique_name in self.__schedulers:
            scheduler_list.append((board_unique_name, self.__schedulers[board_unique_name]))
        if self.__sort_mode == SortModes.RANDOM:
            print("DSADSA")
            return scheduler_list[randint(0, len(scheduler_list) - 1)][1].get_next_pin()
        elif self.__sort_mode == SortModes.ALHABETIC:
            scheduler_list.sort(key=lambda x: x[0])
            pin = scheduler_list[self.__current_scheduler_index - 1][1].get_next_pin()
            self.__current_scheduler_index = (self.__current_scheduler_index + 1) % len(scheduler_list)
            self.__save_to_file()
            return pin
        
        raise Exception(f"Unknown sort mode {self.__sort_mode}")

    def change_accept_time_hour(self, new_hour: int) -> None:
        self.__accept_time = datetime.time(new_hour, 0, 0)
        self.__save_to_file()

    def __load_from_file(self) -> None:
        for board_unique_name in os.listdir(self.channel_cache_folder_path):
            scheduler_path = self.channel_cache_folder_path + '/' + board_unique_name
            if board_unique_name == str(self.__channel_id):
                with open(f"{self.channel_cache_folder_path}/{self.__channel_id}", "r") as cache_file:
                    data = cache_file.read().split('\n')
                    self.__current_scheduler_index = int(data[0])
                    self.__sort_mode = SortModes[data[1]]
                    self.__accept_time = datetime.time.fromisoformat(data[2])
                continue
            
            if os.path.isfile(scheduler_path):
                board_owner, board_name = board_unique_name.split(' ')
                scheduler = PinterestBoardScheduler(self.__board_pool.link_board(board_owner, board_name), scheduler_path)
                self.__schedulers[board_unique_name] = scheduler
    
    def __save_to_file(self) -> None:
        with open(f"{self.channel_cache_folder_path}/{self.__channel_id}", "w") as cache_file:
            cache_file.write(str(self.__current_scheduler_index) + '\n')
            cache_file.write(self.__sort_mode.name + '\n')
            cache_file.write(str(self.__accept_time))
