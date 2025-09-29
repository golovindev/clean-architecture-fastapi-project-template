# Docker Setup для Antiques

Этот документ описывает настройку и использование Docker для приложения Antiques.

## Команды Docker

### Сборка образов

```bash
# Production образ
make docker-build

# Development образ
make docker-build-dev

# Testing образ
make docker-build-test
```

### Запуск сервисов

```bash
# Запуск всех сервисов (production)
make docker-up

# Запуск development окружения
make docker-up-dev

# Остановка всех сервисов
make docker-down
```

### Работа с базой данных

```bash
# Запуск миграций
make docker-migrate

# Подключение к базе данных
docker-compose exec postgres psql -U antiques_user -d antiques
```

### Тестирование

```bash
# Запуск тестов в Docker
make docker-test

# Просмотр отчетов о покрытии
docker-compose --profile test run --rm test
```

### Отладка

```bash
# Просмотр логов
make docker-logs

# Логи только приложения
make docker-logs-app

# Подключение к контейнеру
make docker-shell
```

## Docker Compose Profiles

### production (по умолчанию)
- app (production)
- postgres
- redis

### dev
- app-dev (с hot reload)
- postgres (с exposed портами)
- redis (с exposed портами)

### migrate
- migrate (запуск миграций)

### test
- test (запуск тестов)

### dev-tools
- adminer (веб-интерфейс для БД)

## Переменные окружения

### Обязательные
- `DATABASE_URL` - URL подключения к PostgreSQL
- `REDIS_URL` - URL подключения к Redis

### Опциональные
- `ENVIRONMENT` - окружение (production/development/testing)
- `LOG_LEVEL` - уровень логирования
- `API_HOST` - хост для API
- `API_PORT` - порт для API
- `API_WORKERS` - количество worker процессов

## Volumes

### Named Volumes
- `postgres_data` - данные PostgreSQL
- `redis_data` - данные Redis
- `app_logs` - логи приложения
- `test_reports` - отчеты тестов

### Bind Mounts (development)
- `./src:/app/src` - исходный код
- `./tests:/app/tests` - тесты
- `./alembic:/app/alembic` - миграции

## Сетевые настройки

Все сервисы подключены к сети `antiques-network` для изоляции.

## Health Checks

Все сервисы имеют health checks:
- **app**: HTTP запрос к `/api/docs`
- **postgres**: `pg_isready`
- **redis**: `redis-cli ping`

## Мониторинг

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f app
```
