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


class HeadHunter(API):
    """Класс для получения данных о вакансиях с сайта HeadHunter"""
    def __init__(self, keyword):
        self.__params = {
            "text": keyword,
            "page": 0,
            "per_page": 10
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        formatted_salary = [None, None]
        if salary and salary['from'] and salary['from'] != 0:
            formatted_salary[0] = salary['from'] if salary['currency'].lower() == 'rur' else salary['from']
        if salary and salary['to'] and salary['to'] != 0:
            formatted_salary[1] = salary['to'] if salary['currency'].lower() == 'rur' else salary['to']
        return formatted_salary

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies', params=self.__params)
        return response.json()['items']

    def get_vacancies(self, pages_count=1):
        values = self.get_request()
        self.__vacancies.extend(values)

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'api': 'HeadHunter'
            })
        return formatted_vacancies