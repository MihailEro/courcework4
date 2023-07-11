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
            "text": keyword,  # слово по которому происходит запрос
            "page": 0,  # Номер страницы с которой берутся вакансии
            "per_page": 10  # Колличество вакансий на странице
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
        """Возвращает список вакансий с нужными нами параметрами"""
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


class SuperJob(API):
    """Класс для получения данных о вакансиях с сайта SuperJob"""
    def __init__(self, keyword):
        self.__header = {'Host': 'api.superjob.ru',
                         'X-Api-App-Id': 'v3.r.137653568.b73434bb17b7e24ead0ef381257188069e18874d.1efe2061c3488e60e3aa8f5d7ac3399982ef5934'
                         }
        self.__params = {
            "text": keyword,  # слово по которому происходит запрос
            "page": 0,  # Номер страницы с которой берутся вакансии
            "count": 10  # колличество вакансий на странице
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary, currency):
        formatted_salary = None
        if salary and salary != 0:
            formatted_salary = salary if currency == 'rub' else salary
        return formatted_salary

    def get_request(self):
        response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=self.__header, params=self.__params)
        return response.json()['objects']

    def get_vacancies(self, pages_count=1):
        values = self.get_request()
        self.__vacancies.extend(values)

    def get_formatted_vacancies(self):
        """Возвращает список вакансий с нужными нами параметрами"""
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'salary_from': self.get_salary(vacancy['payment_from'], vacancy['currency']),
                'salary_to': self.get_salary(vacancy['payment_to'], vacancy['currency']),
                'employer': vacancy['firm_name'],
                'api': 'Superjob'
            })
        return formatted_vacancies