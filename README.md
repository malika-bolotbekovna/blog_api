# Blog REST API

Простой REST API для блога на Django REST Framework с поддержкой пользователей, постов и комментариев.

## 📌 Оглавление
- [Особенности](#-особенности)
- [Технологии](#-технологии)
- [Установка](#-установка)
  - [С Docker](#1-запуск-с-docker-рекомендуется)
  - [Локально](#2-запуск-локально-без-docker)
- [Модели](#-модели)
- [API Endpoints](#-api-endpoints)
- [Аутентификация](#-аутентификация)
- [Права доступа](#-права-доступа)
- [Документация](#-документация)
- [Тестирование](#-тестирование)
- [Контакты](#-контакты)

## 🌟 Особенности
- Полный CRUD для постов и комментариев
- token-auth аутентификация
- Права доступа на уровне авторов
- Пагинация
- Автоматическая документация (Swagger/ReDoc)
- Готовый Docker-образ
- Поддержка PostgreSQL

## 💻 Технологии
- Python 3.10+
- Django 4.2+
- Django REST Framework
- Token Authentication (DRF TokenAuth)
- PostgreSQL
- Docker
- Swagger/OpenAPI

## 🚀 Установка

### 1. Запуск с Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com/malika-bolotbekovna/blog_api
cd rest_api

# Построить образ из Dockerfile (в текущей папке):
docker build .

# Собрать и запустить контейнеры
docker-compose up --build

# Выполнить миграции
docker-compose exec web python manage.py migrate

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser
```


### 2. Запуск локально (без Docker)

1. Установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. Настройте базу данных PostgreSQL и создайте файл `.env`:
```ini
NAME_DB=blog_data
USER_DB=blog_data_user
PASSWORD_DB=yourpassword
HOST_DB=localhost
PORT_DB=5432
SECRET=yoursecretkey
DEBUG=on
```

3. Выполните миграции и запустите сервер:
```bash
python manage.py migrate
python manage.py runserver
```

## 🗃️ Модели
### Post
- `id` - UUID
- `author` - FK to User
- `title` - CharField (max_length=50)
- `body` - TextField
- `created_at` - DateTimeField (auto_now_add)
- `updated_at` - DateTimeField (auto_now)
- `is_published` - BooleanField (default=True)

### Comment
- `id` - UUID
- `post` - FK to Post
- `author` - FK to User
- `body` - TextField
- `created_at` - DateTimeField (auto_now_add)
- `updated_at` - DateTimeField (auto_now)
- `is_approved` - BooleanField (default=False)

## 🔌 API Endpoints

| Метод  | Endpoint                      | Описание                      | Аутентификация |
|--------|-------------------------------|-------------------------------|----------------|
| GET    | `/api/v1/posts/`              | Получить список постов        | Не требуется   |
| POST   | `/api/v1/posts/`              | Создать новый пост            | Требуется      |
| GET    | `/api/v1/posts/{id}/`         | Получить пост по ID           | Не требуется   |
| PUT    | `/api/v1/posts/{id}/`         | Обновить пост                 | Только автор   |
| DELETE | `/api/v1/posts/{id}/`         | Удалить пост                  | Только автор   |
| GET    | `/api/v1/comments/`           | Получить все комментарии      | Не требуется   |
| POST   | `/api/v1/posts/{id}/comments/`| Добавить комментарий к посту  | Требуется      |
| POST   | `/api/v1/user/registration/`  | Регистрация                   | Не требуется   |
| POST   | `/api/v1/user/authorization/` | Авторизация                   | Требуется      |

## 🔐 Аутентификация
Используется JWT-аутентификация:
```bash
# Получить токен
POST /api/v1/token/
{
    "username": "your_username",
    "password": "your_password"
}

# Обновить токен
POST /api/v1/token/refresh/
{
    "refresh": "your_refresh_token"
}
```

## 🛡️ Права доступа
- **Гости**: только чтение
- **Авторизованные пользователи**: создание постов/комментариев
- **Авторы**: полный доступ к своим постам/комментариям
- **Администраторы**: полный доступ ко всему

## 📖 Документация
Доступна после запуска проекта:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## 🧪 Тестирование
```bash
# Запуск тестов
docker-compose exec web python manage.py test
# Или локально
python manage.py test
```

## 📬 Контакты
Автор: [Ваше имя]  
Email: your.email@example.com  
GitHub: [yourusername](https://github.com/yourusername)
