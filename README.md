# Парсер книг с сайта tululu.org

С помощью парсера можно скачать книги с сайта [tululu](https://tululu.org/).

Онлайн-версия каталога книг жанра фантастики доступна по [адресу](https://semellot.github.io/books-library-restyle/pages/index1.html)

## Как установить
1. Клонировать репозиторий:

    ```shell
    git clone https://github.com/semellot/books-library-restyle
    ```

2. Установить зависимости:

    ```shell
    pip install -r requirements.txt
    ```

## Парсер книг
Для запуска скрипта используйте команду:
    ```shell
    python parse_tululu_category.py
    ```

По умолчанию скачиваются книги со всех страниц категории фантастики.

Параметры для запуска скрипта:
- --start_page - Начало диапазона страниц для скачивания книг
- --end_page - Конец диапазона страниц для скачивания книг
- --dest_folder - Путь к каталогу с картинками и книгами
- --skip_imgs - Не скачивать картинки
- --skip_txt - Не скачивать книги
- --json_path - Путь к json

## Каталог книг
Для запуска скрипта используйте команду:
    ```shell
    python render_website.py
    ```

Скрипт генерирует страницы html для просмотра списка книг жанра фантастики.
Чтобы открыть каталог оффлайн, откройте адрес в браузере во время работы скрипта [127.0.0.1:5500](http://127.0.0.1:5500/)

Параметры для запуска скрипта:
- --json_path - Путь к json, с информацией о книгах


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков
[dvmn.org](dvmn.org).
