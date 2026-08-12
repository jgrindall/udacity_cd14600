
class Db:
    def __init__(self):
        self.orders = []


class DatabaseConnection:
    _instance = None

    def __new__(cls, connection_string):
        if cls._instance is None:
            print("No instance exists yet")
            instance = super().__new__(cls)
            cls._instance = instance
        else:
            print("Instance already exists")
        return cls._instance

    def __init__(self, connection_string):
        print(f"Initializing DatabaseConnection with connection string: {connection_string}")
        print(f"Current instance connection string: {getattr(self, 'connection_string', None)}")
        print("self is ", self)
        if not hasattr(self, 'connection_string'):
            self.connection_string = connection_string

    def query(self, sql):
        return f"Executing '{sql}' on {self.connection_string}"



class ConfigManager:
    _instance = None

    def __new__(cls, config_file):
        if cls._instance is None:
            print("No instance exists yet")
            instance = super().__new__(cls)
            cls._instance = instance
        else:
            print("Instance already exists")
        return cls._instance

    def __init__(self, config_file):
        print(f"Initializing ConfigManager with config file: {config_file}")
        print(f"Current instance config file: {getattr(self, 'config_file', None)}")
        print("self is ", self)
        if not hasattr(self, 'config_file'):
            self.config_file = config_file

    def get_config(self, key):
        return self.config_file.get(key, None)

    def set_config(self, key, value):
        self.config_file[key] = value