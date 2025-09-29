# Использование MyPy в проекте Antiques

## Установка

```bash
# Установка dev зависимостей (включая MyPy)
uv sync --dev

# Или установка только MyPy
uv add --dev mypy
```

## Основные команды

### Проверка типов

```bash
# Проверить весь проект
uv run mypy src/

# Проверить конкретный файл
uv run mypy src/main.py

# Проверить с подробным выводом
uv run mypy src/ --show-error-codes

# Проверить с показом контекста ошибок
uv run mypy src/ --show-error-context

# Проверить только определенные модули
uv run mypy src/application/ src/domain/
```

### Использование Makefile

```bash
# Показать все доступные команды
make help

# Проверить типы
make type-check

# Запустить все проверки (lint + format + type check)
make check

# Запустить CI pipeline
make ci
```

## Конфигурация MyPy

Основная конфигурация MyPy находится в `pyproject.toml` в секции `[tool.mypy]`.

### Основные настройки

- **python_version**: Python 3.12
- **strict**: false (мягкая проверка для начала)
- **ignore_missing_imports**: true (игнорировать отсутствующие импорты)
- **warn_return_any**: true (предупреждать о возврате Any)
- **no_implicit_optional**: true (требовать явного Optional)

### Per-module настройки

```toml
# Более мягкие правила для тестов и примеров
[[tool.mypy.overrides]]
module = [
    "tests.*",
    "examples.*",
]
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = false

# Игнорировать отсутствующие импорты для внешних библиотек
[[tool.mypy.overrides]]
module = [
    "faststream.*",
    "granian.*",
    "structlog.*",
]
ignore_missing_imports = true
```

## Pre-commit интеграция

MyPy автоматически запускается при коммите через pre-commit hooks:

```bash
# Установить pre-commit hooks
pre-commit install

# Запустить hooks на всех файлах
pre-commit run --all-files

# Запустить только mypy
pre-commit run mypy
```
