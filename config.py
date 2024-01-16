import json

class Config():
    __data: dict = None

    @staticmethod
    def create(config_file_path: str) -> None:
        config_file = open(config_file_path, "r")
        Config.__data = json.loads(config_file.read())
        config_file.close()
    
    @staticmethod
    def data() -> dict:
        if Config.__data is None:
            raise Exception("Config object was not initialized, but something tries to access the data!")
        return Config.__data
        
    
