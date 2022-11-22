# Парсер книг с сайта tululu.org

С помощью парсера можно скачать книги с сайта [tululu](https://tululu.org/).


## Как установить
1. Клонировать репозиторий:

    ```shell
    git clone https://github.com/semellot/books-library-restyle
    ```

2. Установить зависимости:

    ```shell
    pip install -r requirements.txt
    ```

## Аргументы
Для запуска скрипта используйте команду:
    ```shell
    python main.py
    ```

По умолчанию скачаются книги с id от 1 до 10.
Можно указать свой диапазон id с книгами.
Для этого нужно запустить скрипт с двумя числами, например:
    ```shell
    python main.py 20 30
    ```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.