# data_access.py

from abc import ABC, abstractmethod

class DataAccessInterface(ABC):
    @abstractmethod
    def fetch_data(self, symbol, start_date, end_date):
        pass

    @abstractmethod
    def save_data(self, data, filename):
        pass

    @abstractmethod
    def save_data_as_json(self, data, filename):
        pass