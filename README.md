# Chaevarka
## Installation

- git clone https://github.com/avdolya/chaevarka.git

- cd chaevarka

- poetry install

- poetry shell

- docker-compose up -d

- Create env file with TEA_RUN__HOST, TEA_RUN__PORT, TEA_DB__URL

## Installation (Вариант с venv и requirements)
   - git clone https://github.com/avdolya/chaevarka.git
   - cd chaevarka 
   - python -m venv .venv 
   - source .venv/bin/activate 
   - pip install --upgrade pip 
   - pip install -r requirements.txt 
   - docker-compose up -d
   - Create env file with TEA_RUN__HOST, TEA_RUN__PORT, TEA_DB__URL
## Documentation

Swagger: http://localhost:8000/docs

## Structure
``` bush
├── chaevarka-server
│   ├── alembic
│   │   ├── versions
│   │   │   ├── 2025_09_26_1431-ba0d85321b8c_initial_tables.py
│   │   │   └── 2025_09_26_1454-5c198eace621_add_tea_make_table.py
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── api
│   │   ├── api_v1
│   │   │   ├── endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── devices.py
│   │   │   │   └── tea_make.py
│   │   │   ├── schemas
│   │   │   │   ├── __init__.py
│   │   │   │   ├── device.py
│   │   │   │   └── tea_make.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── db_helper.py
│   │   │   ├── device.py
│   │   │   └── tea_make.py
│   │   ├── __init__.py
│   │   └── config.py
│   ├── crud
│   │   ├── __init__.py
│   │   ├── devices.py
│   │   └── tea_make.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── tests_tea_make.py
│   ├── alembic.ini
│   └── main.py
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── README.md
```
## API Endpoints

### Devices

### GET /api/v1/devices/{device_id}
Получает IP-адрес устройства по его уникальному идентификатору (device_id).

### POST /api/v1/devices
Регистрирует новое устройство или обновляет IP-адрес существующего.

-----

### Tea_make

### POST /api/v1/tea-make
Отправляем параметры напитка на сервер

### GET /api/v1/tea-make/{device_id}
Ищем заказы по device_id

### POST /api/v1/tea-make/{order_id}/complete
После выполнения заказа находим его id в бд и меняем статус

### GET /api/v1/tea-make/{order_id}/status
Смотрим статус заказа по id заказа 

-----

## Логика
1. Создание заказа. 
    - Приложение отправляет параметры напитка на сервер. 
    - Сервер создает в базе данных новую запись в таблице tea_make, ей автоматически присваивается id (например, 589). 
    - Сервер устанавливает поле status этой записи в значение 'waiting' 
    - Сервер отвечает приложению (пример): {"status": "success", "order_id": 589} 
    - Приложение получает ответ от сервера и сохраняет число 589 у себя в памяти


2. Опрос чаеваркой. 
    - Чаеварка периодически (раз в 5 сек) обращается к серверу 
    - Сервер выполняет запрос к базе данных: "Найди мне запись, где device_id равен ID чаеварки, а status равен 'waiting'". 
    - Если такая запись найдена, сервер готовится её отдать.


3. Выдача команды и смена статуса. 
   - Перед тем как отдать найденную команду чаеварке, сервер немедленно меняет статус этой записи с 'waiting' на 'in_progress'. 
   - Только после этого сервер отправляет параметры чаеварке.
 
  
4. Завершение цикла.
    - Чаеварка выполняет команду. 
    - После выполнения чаеварка отправляет на сервер отчет: "Заказ №X выполнен". 
    - Сервер находит в базе запись с указанным ID и меняет её статус с 'in_progress' на 'completed'.


5. Получения рез-та в приложении.
   - Приложение стучится на сервер, смотрит выполнен ли заказ с order_id. 
   - При получении статуса 'completed' приложение удаляет заказ из локального хранилища
