from abc import ABC, abstractmethod
import requests

class API(ABC):
    """Абстрактный класс для классов получения данных с сайтов о вакансиях"""
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass