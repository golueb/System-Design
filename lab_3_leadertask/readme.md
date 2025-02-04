## Описание

Разработать приложение для управления целями и задачами, которое должно содержать следующие данные:

- **Цель**
- **Задача**
- **Исполнитель**

## Требования к API

- **Создание нового пользователя**
- **Поиск пользователя по логину**
- **Поиск пользователя по маске имени и фамилии**
- **Создание новой цели**
- **Получение списка всех целей**
- **Создание новой задачи на пути к цели**
- **Получение всех задач цели**
- **Изменение статуса задачи в цели**

# Задание лабораторной работы N3

## Описание

Создайте сервис на Python, который реализует сервисы, спроектированные в первом задании (по проектированию). Должно быть реализовано как минимум два сервиса: управление пользователем и хотя бы один «бизнес» сервис.

## Требования

1. **Сервис должен поддерживать аутентификацию с использованием JWT-token.**
2. **Сервис должен реализовывать как минимум GET/POST методы.**
3. **Данные сервиса должны храниться в памяти.**
4. **В целях проверки должен быть заведён мастер-пользователь (имя admin, пароль secret).**
5. **Данные должны храниться в СУБД PostgreSQL.**
6. **Должны быть созданы таблицы для каждой сущности из вашего задания.**
7. **Должен быть создан скрипт по созданию базы данных и таблиц, а также наполнению СУБД тестовыми значениями.**
8. **Для сущности, должны быть созданы запросы к БД (CRUD) согласно ранее разработанной архитектуре.**
9. **Данные о пользователе должны включать логин и пароль. Пароль должен храниться в закрытом виде (хэширован) – в этом задании опционально.**
10. **Должно применяться индексирования по полям, по которым будет производиться поиск.**

## Результат

- `readme.md` – с текстом задания
- `jwt.py` – основной файл с реализацией сервиса
- `pd_db.py` – инициализация и заполнение тестовыми данными базы данных
- `docker-compose.yml`
- `Dockerfile`
- `openapi.json`
- `requirements.txt`
