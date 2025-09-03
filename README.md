# Chaevarka
## Installation

- git clone https://github.com/avdolya/chaevarka.git

- cd chaevarka

- poetry install

- poetry shell

- docker-compose up -d

- Create env file with TEA_RUN__HOST, TEA_RUN__PORT, TEA_DB__URL

## Documentation

Swagger: http://localhost:8000/docs

## Structure
``` bush
chaevarka/
├── chaevarka-server/          # Основное приложение
│   ├── api/
│   │   └── api_v1/
│   │       ├── endpoints/     # API endpoints
│   │       │   └── devices.py
│   │       ├── schemas/       # Pydantic схемы
│   │       │   └── device.py
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py         # Настройки приложения
│   │   └──  models/           # SQLAlchemy модели
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── device.py
│   │       └── db_helper.py
│   ├── crud/                 # Бизнес-логика
│   │   └── devices.py
│   ├── alembic/              # Миграции базы данных
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   └── main.py               # Точка входа
├── docker-compose.yml        # Docker конфигурация
├── poetry.lock               # Lock-файл зависимостей Poetry
├── pyproject.toml            # Конфигурация Poetry
└── README.md                 # Документация
```
## API Endpoints

### GET /api/v1/devices/{device_id}
Получает IP-адрес устройства по его уникальному идентификатору (device_id).

### POST /api/v1/devices
Регистрирует новое устройство или обновляет IP-адрес существующего.
