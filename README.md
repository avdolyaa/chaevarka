# Chaevarka — Backend Server

Backend сервер для умной чаемашины ТиВайб. Мобильное приложение отправляет параметры напитка, сервер ставит заказ в очередь, устройство забирает и выполняет, затем сообщает о завершении.

**Продакшен:** https://teavibe.site

## Стек

- **FastAPI** + async SQLAlchemy (asyncpg) + PostgreSQL
- **fastapi-users** — авторизация, верификация email, сброс пароля
- **Alembic** — миграции БД
- **Jinja2** + aiosmtplib — транзакционные письма
- **Docker** + Nginx + Certbot (TLS)

## Быстрый старт (локально)

```bash
git clone https://github.com/avdolya/chaevarka.git
cd chaevarka

# Создать .env на основе примера и заполнить
cp .env.example .env

# Поднять все сервисы (postgres, api, nginx, maildev)
docker-compose up -d

# Применить миграции
docker-compose exec api alembic upgrade head
```

Swagger UI: http://localhost/docs  
Maildev (перехват писем): http://127.0.0.1:1080

## Запуск в продакшене

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker-compose exec api alembic upgrade head
```

## Переменные окружения

Все переменные с префиксом `TEA_`, вложенность через `__`. Полный список в `.env.example`.

| Переменная | Описание |
|---|---|
| `TEA_DB__URL` | PostgreSQL DSN |
| `TEA_ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET` | Секрет для токенов сброса пароля |
| `TEA_ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET` | Секрет для токенов верификации |
| `TEA_SUPERUSER__EMAIL` | Email суперпользователя |
| `TEA_SUPERUSER__PASSWORD` | Пароль суперпользователя |
| `TEA_SMTP__HOST` | SMTP хост (локально: `maildev`, прод: `smtp.yandex.ru`) |
| `TEA_SMTP__PORT` | SMTP порт (локально: `1025`, прод: `465`) |
| `TEA_SMTP__USE_TLS` | TLS (локально: `false`, прод: `true`) |
| `TEA_DOCS_PASSWORD` | Пароль для Swagger UI |

## API Endpoints

Все эндпоинты с префиксом `/api/v1`.

Обозначения: `—` публичный · `токен` Bearer-токен активного пользователя · `суперпользователь` только суперпользователь

### Auth
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| POST | `/auth/login` | Получить токен доступа | — |
| POST | `/auth/logout` | Выйти | токен |
| POST | `/auth/register` | Зарегистрироваться | — |
| POST | `/auth/verify` | Подтвердить email | — |
| POST | `/auth/forgot-password` | Запросить сброс пароля | — |
| POST | `/auth/reset-password` | Сбросить пароль | — |

### Users
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| GET | `/users/me` | Получить текущего пользователя | токен |
| PATCH | `/users/me` | Обновить профиль | токен |
| DELETE | `/users/me` | Удалить аккаунт | токен |

### Devices
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| GET | `/devices/{device_id}` | Получить устройство по ID | — |
| POST | `/devices` | Зарегистрировать или обновить устройство | — |
| DELETE | `/devices` | Удалить все устройства | суперпользователь |

### Tea Make (заказы)
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| POST | `/tea-make` | Создать заказ | токен |
| GET | `/tea-make/{device_id}` | Забрать заказ (устройство) — меняет статус на `in_progress` | — |
| GET | `/tea-make/order/{order_id}` | Получить заказ по ID | — |
| GET | `/tea-make/{order_id}/status` | Статус заказа | — |
| POST | `/tea-make/{order_id}/complete` | Завершить заказ | — |
| POST | `/tea-make/{order_id}/cancel` | Отменить заказ | токен |
| POST | `/tea-make/{order_id}/dispense` | Выдать напиток | токен |
| PATCH | `/tea-make/{order_id}/status` | Изменить статус | — |
| DELETE | `/tea-make` | Удалить все заказы | суперпользователь |

### Recipes
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| GET | `/recipes/` | Все рецепты | — |
| GET | `/recipes/my` | Рецепты текущего пользователя | токен |
| POST | `/recipes/` | Создать рецепт | токен |
| PATCH | `/recipes/{recipe_id}` | Обновить рецепт | токен |
| DELETE | `/recipes/{recipe_id}` | Удалить рецепт | токен |

### Drums
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| GET | `/drums/config` | Конфигурация барабанов | — |
| POST | `/drums/config` | Обновить конфигурацию | суперпользователь |

### Firmware
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| POST | `/upload` | Загрузить прошивку | суперпользователь |
| GET | `/devices/{device_id}/check-update` | Проверить наличие обновления | — |
| GET | `/devices/firmware/download/{firmware_id}` | Скачать прошивку | — |

### Health
| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| GET | `/ping` | Проверка сервера | — |
| GET | `/health` | Проверка сервера + БД | — |

## Схема базы данных

```
users
├── id (PK)
├── email, hashed_password, is_active, is_verified
├── first_name, last_name, phone, profile_picture
└── device_id → FK → devices.device_id (SET NULL)

devices
├── id (PK)
├── device_id (unique)
├── ip_address
└── online_at

tea_make
├── id (PK)
├── device_id             — к какому устройству заказ
├── status                — waiting → in_progress → completed
├── water, water_for_cup, temperature, time, tea_cnt, type
└── drum_1 … drum_6       — количество ингредиентов из каждого барабана

drum_config
├── id (PK)
└── ingredient_name       — что насыпано в барабан (по позиции)

recipes
├── id (PK)
├── user_id → FK → users.id (CASCADE)
├── title, description, type, icon, is_public
├── water_amount, temperature, time, tea_amount
└── drum_1 … drum_6

firmware
├── id (PK)
├── version (unique)
├── device_prefix
└── file_path

accesstoken
├── id (PK)
├── token, created_at, expires_at
└── user_id → FK → users.id (CASCADE)
```

**Связи:**
- `users` → `devices`: много-к-одному (несколько пользователей могут использовать одно устройство)
- `recipes` → `users`: много-к-одному (рецепты принадлежат пользователю, удаляются вместе с ним)
- `accesstoken` → `users`: много-к-одному (у пользователя может быть несколько токенов)

## Логика заказа

```
waiting → in_progress → completed
```

1. Приложение создаёт заказ — статус `waiting`, сервер возвращает `order_id`
2. Устройство опрашивает сервер раз в 5 сек — сервер атомарно меняет статус на `in_progress` и отдаёт параметры
3. Устройство выполняет заказ и отправляет `complete` — статус меняется на `completed`
4. Приложение видит `completed` и удаляет заказ локально

## Структура проекта

```
chaevarka/
├── chaevarka-server/
│   ├── api/api_v1/
│   │   ├── endpoints/      — роутеры (auth, users, devices, tea_make, recipes, drums, firmware, health)
│   │   └── schemas/        — Pydantic схемы
│   ├── core/
│   │   ├── config.py       — настройки (pydantic-settings)
│   │   └── models/         — SQLAlchemy модели
│   ├── crud/               — запросы к БД
│   ├── mailing/            — отправка писем
│   ├── templates/          — Jinja2 HTML шаблоны писем
│   ├── views/              — HTML страницы (верификация, сброс пароля)
│   └── alembic/            — миграции
├── frontend/               — статический лендинг
├── nginx-configs/
│   ├── default.conf        — nginx для продакшена (HTTPS)
│   └── local.conf          — nginx для локалки (HTTP)
├── build-app/nginx/
│   ├── Dockerfile          — образ nginx для прода
│   └── Dockerfile.local    — образ nginx для локалки
├── docker-compose.yml      — база (pg, api)
├── docker-compose.override.yml  — локалка (maildev, nginx без SSL)
├── docker-compose.prod.yml — прод (certbot, nginx с SSL)
└── .env.example            — шаблон переменных окружения
```
