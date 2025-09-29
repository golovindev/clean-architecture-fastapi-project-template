# Использование Ruff в проекте Antiques

## Установка

```bash
# Установка dev зависимостей (включая Ruff)
uv sync --dev

# Или установка только Ruff
uv add --dev ruff
```

## Основные команды

### Проверка кода (linting)

```bash
# Проверить весь проект
uv run ruff check src/ tests/

# Проверить конкретный файл
uv run ruff check src/main.py

# Проверить с подробным выводом
uv run ruff check src/ tests/ --verbose

# Проверить только определенные правила
uv run ruff check src/ --select E,F,W

# Игнорировать определенные правила
uv run ruff check src/ --ignore E501,W503
```

### Автоматическое исправление

```bash
# Исправить все автоматически исправляемые проблемы
uv run ruff check --fix src/ tests/

# Исправить только определенные правила
uv run ruff check --fix --select E,F src/

# Показать, что будет исправлено, без фактического исправления
uv run ruff check --fix --diff src/
```

### Форматирование кода

```bash
# Отформатировать весь проект
uv run ruff format src/ tests/

# Проверить форматирование без изменений
uv run ruff format --check src/ tests/

# Показать diff форматирования
uv run ruff format --diff src/
```

### Комплексная проверка

```bash
# Проверить и исправить все проблемы
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Или одной командой (если настроено в pyproject.toml)
uv run ruff check --fix src/ tests/ && uv run ruff format src/ tests/
```

## Использование Makefile

```bash
# Показать все доступные команды
make help

# Установить dev зависимости
make install-dev

# Проверить код
make lint

# Исправить проблемы автоматически
make lint-fix

# Отформатировать код
make format

# Запустить все проверки
make check

# Запустить тесты
make test

# Запустить тесты с покрытием
make test-cov

# Очистить кэш
make clean

# Настроить dev окружение
make dev-setup

# Запустить CI pipeline
make ci
```

## Pre-commit hooks

```bash
# Установить pre-commit hooks
pre-commit install

# Запустить hooks на всех файлах
pre-commit run --all-files

# Обновить hooks
pre-commit autoupdate
```
