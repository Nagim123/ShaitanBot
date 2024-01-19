import os
from random import shuffle, randint
from pinterest_board_parser.pinterest_board import PinterestBoard
from pinterest_board_parser.pinterest_pin import PinterestPin
from pin_scheduling.no_more_pins_exception import NoMorePinsException

class PinterestBoardScheduler:
    def __init__(self, board: PinterestBoard, save_file_path: str) -> None:
        self.__board = board
        self.__save_file_path = save_file_path

        if os.path.exists(save_file_path):
            self.__load_from_file()
        else:
            self.__pin_count = len(board.get_pins())
            self.__scheduled_pin_indexes = [i for i in range(self.__pin_count)]
            shuffle(self.__scheduled_pin_indexes)
            self.__current_pin_index = 0
            self.__save_to_file()

    def get_next_pin(self) -> PinterestPin:
        if self.__current_pin_index >= len(self.__scheduled_pin_indexes):
            raise NoMorePinsException()
        
        pin_index = self.__scheduled_pin_indexes[self.__current_pin_index]
        parsed_pins = self.__board.get_pins()
        
        print(pin_index)
        print(self.__pin_count)
        print(len(parsed_pins))
        for i in range(self.__pin_count, len(parsed_pins)):
            self.__scheduled_pin_indexes.insert(randint(0, self.__pin_count-1), i)
        self.__current_pin_index += 1
        
        self.__save_to_file()
        return parsed_pins[pin_index]
    
    def __load_from_file(self) -> None:
        with open(self.__save_file_path, "r") as save_file:
            data = save_file.read().split('\n')
            self.__pin_count = int(data[0])
            self.__current_pin_index = int(data[1])
            self.__scheduled_pin_indexes = [int(x) for x in data[2].split(',')]

    def __save_to_file(self) -> None:
        with open(self.__save_file_path, "w") as save_file:
            save_file.write(str(self.__pin_count) + '\n')
            save_file.write(str(self.__current_pin_index) + '\n')
            schedule_str = str(self.__scheduled_pin_indexes[0])
            for i in range(1, len(self.__scheduled_pin_indexes)):
                schedule_str += f', {self.__scheduled_pin_indexes[i]}'
            save_file.write(schedule_str + '\n')
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PinterestBoardScheduler):
            return self.__save_file_path == __value.__save_file_path
        return False