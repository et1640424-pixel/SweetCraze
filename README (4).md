# Sweet Craze — REST API магазина тортов и выпечки

Backend онлайн-магазина кондитерских изделий на **Django + Django REST Framework**: пекарни, категории, товары с несколькими фото, заказы со статусами, корзина и авторизация.

## Возможности

- Регистрация, вход и выход, вход через Google (`django-allauth`)
- Профиль пользователя: имя, телефон, возраст, аватар, страна, город, адрес
- Пекарни (`Bakery`) с адресом и изображением
- Категории с описанием и изображением, товары (цена, вес, наличие, фото)
- Фильтры и пагинация товаров
- Заказы (`Order`) со статусами `active` / `completed` / `canceled`, датами заказа и выполнения
- Корзина и позиции корзины (создание, изменение количества, удаление)
- Swagger-документация (`drf-yasg`)
- Docker: gunicorn + nginx + PostgreSQL

## Стек

Python 3.12 · Django · DRF · SimpleJWT · django-allauth · django-filter · django-phonenumber-field · drf-yasg · django-cors-headers · Pillow · Docker / nginx / gunicorn

## Структура

```
Sweet_craze/
└── mysite/
    ├── manage.py
    ├── req.txt
    ├── .env                      # SECRET_KEY
    ├── Dockerfile, docker-compose.yml.yaml
    ├── nginx/                    # Dockerfile и nginx.conf
    ├── mysite/                   # настройки проекта
    └── cake_shop/                # основное приложение
        ├── models.py             # UserProfile, Bakery, Category, Product,
        │                         # ProductImage, Order, Cart, CartItem
        ├── views.py, serializers.py, urls.py
        ├── filters.py, pagination.py
        └── migrations/
```

## Быстрый старт

```bash
cd mysite
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r req.txt
```

Создайте `.env` рядом с `manage.py`:

```
SECRET_KEY=ваш-секретный-ключ
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сервер: http://127.0.0.1:8000/en/ · Админка: http://127.0.0.1:8000/en/admin/

> Маршруты обёрнуты в `i18n_patterns`, поэтому URL начинаются с языкового префикса (`/en/`).

## Запуск через Docker

```bash
cd mysite
docker compose -f docker-compose.yml.yaml up --build
```

Приложение будет доступно на порту 80 через nginx. Путь `/home/ubuntu/Sweet_craze/mysite/staticfiles` в compose-файле замените на свой.

## Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/register/`, `/login/`, `/logout/` | Авторизация |
| GET | `/user/`, `/user/<id>` | Пользователи |
| GET | `/bakery/`, `/bakery/<id>` | Пекарни |
| GET | `/category/`, `/category/<id>` | Категории |
| GET | `/product/`, `/product/<id>` | Товары |
| GET | `/order/`, `/order/<id>` | Заказы |
| GET | `/cart/` | Корзина |
| GET, POST / PUT, DELETE | `/cart_item/`, `/cart_item/<id>/` | Позиции корзины |

## Заметки

- В `settings.py` стоит **SQLite**; PostgreSQL из `docker-compose` пока не подключён.
- Не публикуйте `.env` и `db.sqlite3` в открытом репозитории.
