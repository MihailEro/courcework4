from src.classes import HeadHunter, SuperJob
from src.saver import Saver


def main():
    vacancies_json = []  # Пустой словарь для записи вакансий полученых с HH и SJ
    keyword = input('Введите запрос для поиска профессии: ')  # Ключевое слово для поиска профессий
    hh = HeadHunter(keyword)  # Экземпляр класса HeadHunter
    sj = SuperJob(keyword)  # Экземпляр класса SuperJob

    for api in (hh, sj):
        api.get_vacancies(pages_count=3)  # Количество обрабытываемых страниц(pages_count)
        vacancies_json.extend(api.get_formatted_vacancies())

    saver = Saver(keyword=keyword, vacancies_json=vacancies_json)  # Экземпляр класса Saver

    while True:
        command = input(
            "1 - Вывести список вакансий; \n"
            "2 - Сортировать вакансии по минимальной зарплате (убывание); \n"
            "exit - Выход.\n"
        ) # Выбор действия со списком вакансий
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = saver.select()
        elif command == '2':
            vacancies = saver.sort_vacancies_by_salary_from_desk()

        for vacancy in vacancies:
            print(vacancy, end='\n\n')


if __name__ == '__main__':
    main()