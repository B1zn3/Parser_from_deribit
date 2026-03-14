# Deribit Price Tracker

Приложение раз в минуту получает с биржи Deribit текущие index price для `btc_usd` и `eth_usd`, сохраняет их в PostgreSQL и предоставляет HTTP API на FastAPI для чтения сохранённых данных.

## Функциональность

- получение цен `btc_usd` и `eth_usd` с Deribit
- сохранение в PostgreSQL:
  - тикер
  - цена
  - время получения в UNIX timestamp
- HTTP API на FastAPI:
  - получение всех сохранённых данных по тикеру
  - получение последней цены по тикеру
  - получение цен по тикеру с фильтром по времени
- фоновый запуск задачи каждую минуту через Celery
- миграции базы данных через Alembic
- контейнеризация через Docker Compose

## Стек

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Celery
- Redis
- Poetry
- aiohttp
- pytest

## Структура проекта

```text
app/
  api/
    routers/
      prices.py
    schemas/
      price.py
  core/
    config.py
    celery_app.py
    database.py
  domain/
    models/
      price_snapshot.py
    repositories/
      price_repository.py
    services/
      market_data_service.py
  infrastructure/
    clients/
      deribit_client.py
    repositories/
      price_repository_impl.py
  tasks/
    fetch_prices.py
  main.py

migrations/
tests/
docker-compose.yml
Dockerfile
README.md
pyproject.toml

## API
GET /prices?ticker=btc_usd - Получить все сохранённые цены по тикеру
GET /prices/latest?ticker=btc_usd - Получить последнюю цену по тикеру
GET /prices/filter?ticker=btc_usd&from_ts=1773427000000000&to_ts=1773428000000000 - Получить цены по тикеру с фильтром по времени

## Переменные окружения
Создай файл .env в корне проекта как .env.example.

## Запуск
Требования:
- Docker Desktop

Команда запуска: 
docker compose up --build

## Что поднимется
db — PostgreSQL
redis — Redis
migrate — контейнер для применения Alembic миграций
api — FastAPI приложение
worker — Celery worker со встроенным beat



