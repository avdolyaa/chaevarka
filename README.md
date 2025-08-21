# Chaevarka
## Installation
git clone https://github.com/avdolya/chaevarka.git

cd chaevarka

poetry install

poetry shell

docker-compose up -d

### Create env file with TEA_RUN__HOST, TEA_RUN__PORT=8000, TEA_DB__URL
## Docs
Swagger: http://localhost:8000/docs
## Structure
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

## API_ENDPOINTS
GET /api/v1/devices
POST /api/v1/devices
