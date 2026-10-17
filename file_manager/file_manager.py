import json
import os

class FileManager:
    def __init__(self, data_dir:str):
        self.__data_dir = data_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @data_dir.setter
    def data_dir(self, value):
        if not isinstance(value, str):
            raise TypeError("data_dir should be a string")
        if not value.strip():
            raise ValueError("data_dir shouldn't be empty")
        self.__data_dir = value


#-------------------------------------------------------------------
# Method to Load data to a file
#-------------------------------------------------------------------

    def load_data(self, filename:str):
        file_path = f"{self.__data_dir}/{filename}"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError("File not found")
        except Exception as e:
            raise Exception(f"Error occurred while loading data: {e}")

# -------------------------------------------------------------------
# Method to Save data to a file
# -------------------------------------------------------------------

    def save_data(self, filename:str, data):
        os.makedirs(self.__data_dir, exist_ok=True)  
        file_path = f"{self.__data_dir}/{filename}"
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            raise Exception(f"Error occurred while saving data: {e}")