# Миграции базы данных

Этот проект использует Alembic для управления миграциями базы данных PostgreSQL.

## Команды для работы с миграциями

### Создание новой миграции
```bash
# Создать миграцию с автогенерацией (требует подключения к БД)
make migration msg="Описание изменений"

# Или напрямую через alembic
uv run alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
# Применить все ожидающие миграции
make migrate

# Или напрямую
uv run alembic upgrade head
```

### Откат миграций
```bash
# Откатить на одну миграцию назад
make migrate-downgrade

# Или напрямую
uv run alembic downgrade -1
```

### Просмотр истории миграций
```bash
# Показать историю миграций
make migrate-history

# Показать текущую миграцию
make migrate-current
```

### Другие полезные команды
```bash
# Отметить БД как находящуюся на определенной миграции (без применения)
make migrate-stamp

# Показать SQL для миграции (без применения)
uv run alembic upgrade head --sql
```

## Структура файлов

- `alembic.ini` - конфигурация Alembic
- `alembic/env.py` - настройки окружения для миграций
- `alembic/versions/` - директория с файлами миграций
- `alembic/script.py.mako` - шаблон для новых миграций
