### API books library - API для книжной бибилиотеки

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/-DRF-464646?style=flat-square&logo=django-rest-framework)](https://www.django-rest-framework.org/)
### Технологии:
- python 3.12
- django 5.1.3
- djangorestframework 3.15.2
- PostgreSQL
- Celery
- Redis
- Docker, Docker Compose

### Инструкция для развертывания проекта:

#### Клонирование проекта:

```bash
git clone https://github.com/KonstantinMikheev/api_for_books_library.git
```

#### Создать виртуальное окружение:

```bash
python3 -m venv venv
```

#### Активировать виртуальное окружение:

```bash
source venv/bin/activate
```

#### Установить зависимости:

```bash
pip install -r pyproject.toml
```

#### Откройте проект в PyCharm, настройте базу данных в settings.py и выполните миграции:

```bash
python3 manage.py migrate
```

#### Для корректной работы проекта, требуется файл .env, который содержит переменные окружения:

Для настройки файла, в корне проекта создайте файл `.env` и заполните его переменными окружения указанными в файле `env.sample`

### Запуск программы

```bash
python3 manage.py runserver
```

#### Чтобы начать рассылку напоминаний в терминале запустите celery worker командой

```bash
celery -A config worker -l INFO
```
#### Команда для windows:

```bash
celery -A config worker -l INFO -P eventlet
```

### Запуск через Docker Compose:

Для запуска всех сервисов выполните команду:
```bash
docker-compose up --build
```
Для запуска в фоновом режиме:
```bash
docker-compose up -d
```
После запуска доступность сервисов можно проверить командой:
```bash
docker-compose ps
```

### Автор проекта Константин Михеев
