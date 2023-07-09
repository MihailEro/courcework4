from src.classes import HeadHunter, SuperJob
from src.saver import Saver


def main():
    vacancies_json = []
    keyword = input('Введите запрос для поиска профессии: ')
    hh = HeadHunter(keyword)
    sj = SuperJob(keyword)

    for api in (hh, sj):
        api.get_vacancies(pages_count=3)
        vacancies_json.extend(api.get_formatted_vacancies())

    saver = Saver(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - Вывести список вакансий; \n"
            "2 - Сортировать вакансии по минимальной зарплате (убывание); \n"
            "exit - Выход.\n"
        )
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = saver.select()
        elif command == '2':
            vacancies = saver.sort_vacancies_by_salary_from_desk()
        elif command == '4':
            vacancies = saver.sort_vacancies_by_salary_to_asc()

        for vacancy in vacancies:
            print(vacancy, end='\n\n')


if __name__ == '__main__':
    main()