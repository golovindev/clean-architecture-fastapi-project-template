# Clean Architecture FastAPI Project Cookiecutter Template

A comprehensive cookiecutter template for creating modern FastAPI applications with clean architecture, Docker support, and best practices included.

## 🚀 Features

- **Clean Architecture**: Domain-Driven Design with clear separation of concerns
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: Modern ORM with async support
- **Database Support**: Optional database support (PostgreSQL/SQLite/MySQL)
- **Alembic**: Database migration management
- **Docker**: Complete containerization with Docker Compose
- **Caching System**: Optional caching support (Redis/KeyDB/Tarantool/Dragonfly)
- **Message Broker**: Optional message broker support (Kafka/RabbitMQ/NATS)
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Ruff for linting, MyPy for type checking
- **Pre-commit**: Git hooks for code quality
- **Documentation**: Auto-generated API docs with Swagger/OpenAPI

## 📋 Prerequisites

- Python 3.12+
- Cookiecutter: `pip install cookiecutter`
- Docker and Docker Compose (optional, for containerized development)

## 🛠️ Usage

### Basic Usage

```bash
cookiecutter https://github.com/Peopl3s/clean-architecture-fastapi-project-template.git
```

### Local Usage

```bash
# Clone the template
git clone https://github.com/Peopl3s/clean-architecture-fastapi-project-template.git
cd clean-architecture-fastapi-project-template

# Use the template
cookiecutter .
```

### Non-interactive Usage

```bash
cookiecutter . --no-input \
  project_name="My Awesome API" \
  project_description="An awesome API for my project" \
  author_name="John Doe" \
  author_email="john@example.com" \
  github_username="johndoe" \
  domain_name="awesomeapi.com" \
  use_broker="kafka" \
  use_cache="redis" \
  use_database="postgresql" \
  add_docker="y" \
  add_tests="y" \
  add_docs="y" \
  add_precommit="y" \
  license_type="MIT"
```

## ⚙️ Template Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `project_name` | Name of the project | "My FastAPI Project" | Yes |
| `project_slug` | Slugified project name (auto-generated) | - | No |
| `project_description` | Short description of the project | "A modern FastAPI application..." | Yes |
| `author_name` | Author's name | "Your Name" | Yes |
| `author_email` | Author's email | "your.email@example.com" | Yes |
| `github_username` | GitHub username | "yourusername" | Yes |
| `version` | Project version | "0.1.0" | No |
| `database_name` | Database name | `{project_slug}` | No |
| `database_user` | Database username | `{project_slug}_user` | No |
| `database_password` | Database password | `{project_slug}_password` | No |
| `redis_password` | Redis password | "redis_password" | No |
| `api_title` | API title | `{project_name} API` | No |
| `api_version` | API version | "1.0.0" | No |
| `api_description` | API description | "API for {project_description}" | No |
| `domain_name` | Domain name for APIs | "example.com" | Yes |
| `use_broker` | Choose message broker type | "none" | No |
| `use_cache` | Choose caching system type | "none" | No |
| `use_database` | Choose database type (none/postgresql/sqlite/mysql) | "none" | No |
| `add_docker` | Add Docker configuration | "y" | No |
| `add_tests` | Add test suite | "y" | No |
| `add_docs` | Add documentation | "y" | No |
| `add_precommit` | Add pre-commit hooks | "y" | No |
| `license_type` | License type | "MIT" | No |

## 🏗️ Generated Project Structure

```
{{cookiecutter.project_slug}}/
├── 📁 src/                          # Source code
│   ├── 📁 domain/                   # Domain layer (business logic)
│   │   ├── 📁 entities/             # Domain entities
│   │   ├── 📁 value_objects/        # Value objects
│   │   ├── 📁 services/             # Domain services
│   │   └── exceptions.py            # Domain exceptions
│   ├── 📁 application/              # Application layer
│   │   ├── 📁 use_cases/            # Use cases
│   │   ├── 📁 dtos/                 # Data transfer objects
│   │   ├── 📁 interfaces/           # Application interfaces
│   │   └── exceptions.py            # Application exceptions
│   ├── 📁 presentation/             # Presentation layer
│   │   └── 📁 api/                  # API endpoints
│   │   └── 📁 cli/                  # CLI endpoints
│   ├── 📁 infrastructures/          # Infrastructure layer
│   │   ├── 📁 db/                   # Database implementations
│   │   ├── 📁 cache/                # Cache implementations
│   │   └── 📁 broker/               # Message broker implementations
│   │   └── 📁 dtos/                 # DTO c Pydantic
│   └── 📁 config/                   # Configuration
│       └── 📁 ioc/                  # Dependency injection
├── 📁 tests/                        # Test suite
├── 📁 alembic/                      # Database migrations
├── 📁 docs/                         # Documentation
├── 📁 scripts/                      # Utility scripts
├── pyproject.toml                   # Project configuration
├── docker-compose.yml               # Docker services
├── Dockerfile                       # Container configuration
├── env.template                     # Environment variables template
├── .pre-commit-config.yaml          # Pre-commit hooks
├── .gitignore                       # Git ignore rules
└── README.md                        # Project documentation
```

## 🚀 Quick Start

### 1. Create Your Project

```bash
cookiecutter https://github.com/Peopl3s/clean-architecture-fastapi-project-template.git
```

### 2. Navigate to Your Project

```bash
cd {{cookiecutter.project_slug}}
```

### 3. Set Up Environment

```bash
cp env.template .env
# Edit .env with your configuration
```

### 4. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 5. Run with Docker (Recommended)

```bash
# Start all services
docker-compose --profile dev up -d

# View logs
docker-compose logs -f
```

### 6. Run Locally

```bash
# Start dependencies (if using Docker for services)
docker-compose up -d postgres redis mysql

# Run migrations
make migrate

# Start the application
uv run python -m src.main
```

## 📚 API Documentation

Once your application is running, access the API documentation at:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/openapi.json`

## 🛠️ Development Commands

### Code Quality

```bash
make lint          # Run linter
make lint-fix     # Fix linting issues
make format        # Format code
make type-check    # Run type checker
make check         # Run all checks
```

### Testing

```bash
make test          # Run tests
make test-cov      # Run tests with coverage
make docker-test   # Run tests in Docker
```

### Database

```bash
make migration msg="Description"  # Create migration
make migrate                      # Apply migrations
make migrate-downgrade            # Rollback migration
```

### Docker

```bash
make docker-build    # Build Docker image
make docker-up-dev   # Start development environment
make docker-down     # Stop all services
make docker-logs     # View logs
```

## 🏗️ Architecture Overview

The template follows **Clean Architecture** principles with clear separation of concerns:

### Domain Layer
- **Entities**: Core business objects
- **Value Objects**: Immutable domain types
- **Services**: Business logic that doesn't fit in entities
- **Exceptions**: Domain-specific exceptions

### Application Layer
- **Use Cases**: Application-specific business rules
- **DTOs**: Data transfer objects using plain dataclasses with validation logic (Pydantic-free)
- **Interfaces**: Abstractions for infrastructure implementations
- **Unit of Work**: Transaction management and coordination
- **Mappers**: Convert between domain entities and DTO objects

### Presentation Layer
- **API Controllers**: Handle HTTP requests
- **Middleware**: Cross-cutting concerns
- **Routers**: URL routing configuration

### Infrastructure Layer
- **Repositories**: Data access implementations
- **Cache**: Caching service implementations
- **Message Brokers**: External service integrations using Pydantic models
- **HTTP Clients**: External API integrations using Pydantic models
- **Infrastructure DTOs**: Pydantic models for external communication and serialization
- **Infrastructure Mappers**: Convert between application DTOs and infrastructure Pydantic models

## 🔧 Configuration

### Environment Variables

The template uses environment variables for configuration. Copy `env.template` to `.env` and customize:

```bash
# Application
ENVIRONMENT=dev
LOG_LEVEL=DEBUG
DEBUG=true

# Database (if enabled)
# PostgreSQL
POSTGRES_USER={{cookiecutter.database_user}}
POSTGRES_PASSWORD={{cookiecutter.database_password}}
POSTGRES_DB={{cookiecutter.database_name}}

# SQLite
SQLITE_DB_PATH={{cookiecutter.database_name}}.db
SQLITE_DB_DIR=./data

# MySQL
MYSQL_USER={{cookiecutter.database_user}}
MYSQL_PASSWORD={{cookiecutter.database_password}}
MYSQL_DB={{cookiecutter.database_name}}

# Redis (if enabled)
REDIS_PASSWORD={{cookiecutter.redis_password}}

# External APIs
MUSEUM_API_BASE=https://api.{{cookiecutter.domain_name}}
CATALOG_API_BASE=https://catalog.{{cookiecutter.domain_name}}
```

### Dependency Injection

The template uses **Dishka** for dependency injection. Providers are configured in `src/config/ioc/providers.py`.

## 🧪 Testing

The template includes a comprehensive test suite:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **API Tests**: Test HTTP endpoints
- **Infrastructure Tests**: Test database and cache operations

Run tests with coverage:
```bash
make test-cov
```

## 🐳 Docker Support

The template includes complete Docker configuration:

- **Development**: Hot-reload development environment
- **Production**: Optimized production build
- **Testing**: Isolated test environment
- **Migrations**: Database migration runner

Services included:
- **Database**: Database support (PostgreSQL, SQLite, or MySQL, optional)
- **Caching System**: Caching support (Redis, KeyDB, Tarantool, or Dragonfly, optional)
- **Message Broker**: Message broker support (Kafka/Zookeeper, RabbitMQ, or NATS, optional)
- **Application**: FastAPI application

## 📝 Customization

### Adding New Features

1. **Domain**: Add entities/value objects in `src/domain/`
2. **Use Cases**: Add use cases in `src/application/use_cases/`
3. **Unit of Work**: Add transaction coordination in `src/application/uow/`
4. **API**: Add controllers in `src/presentation/api/`
5. **Infrastructure**: Add implementations in `src/infrastructures/`

### Implementation Examples

The template includes comprehensive implementation examples that demonstrate best practices:

#### Domain Layer Examples
- **Entity Implementation**: `src/domain/entities/artifact.py` - Shows how to create domain entities with business logic
- **Value Objects**: `src/domain/value_objects/era.py` and `src/domain/value_objects/material.py` - Demonstrates immutable value objects with validation
- **Domain Services**: Examples of business logic that doesn't fit in entities

#### Application Layer Examples
- **Use Cases**: `src/application/use_cases/get_artifact.py` - Shows how to implement business logic using dependency injection
- **DTOs**: `src/application/dtos/artifact.py` - Data transfer objects using plain dataclasses with validation in `__post_init__` methods (Pydantic-free)
- **Interfaces**: Complete interface definitions for repositories, cache, HTTP clients, and message brokers
- **Mappers**: Examples of converting between domain entities and DTOs

#### Infrastructure Layer Examples
- **Repository Implementation**: `src/infrastructures/db/repositories/artifact.py` - Shows how to implement repository pattern with SQLAlchemy
- **Cache Implementation**: `src/infrastructures/cache/redis_client.py` - Redis caching implementation with error handling
- **HTTP Clients**: `src/infrastructures/http/clients.py` - External API integration examples using Pydantic models for external communication
- **Database Models**: `src/infrastructures/db/models/artifact.py` - SQLAlchemy model examples
- **Infrastructure DTOs**: `src/infrastructures/dtos/artifact.py` - Pydantic models for external API communication and serialization
- **Infrastructure Mappers**: `src/infrastructures/mappers/artifact.py` - Mappers for converting between application DTOs and infrastructure Pydantic models

#### Presentation Layer Examples
- **REST Controllers**: `src/presentation/api/rest/v1/controllers/artifact_controller.py` - API endpoint implementation
- **Exception Handling**: `src/presentation/api/rest/v1/exceptions.py` - Custom exception handlers
- **Middleware**: `src/presentation/api/rest/middlewares.py` - Request/response middleware examples

#### Configuration Examples
- **Dependency Injection**: `src/config/ioc/providers.py` - Complete DI container setup
- **Configuration Management**: `src/config/base.py` - Environment-based configuration
- **Logging Setup**: `src/config/logging.py` - Structured logging configuration

#### Testing Examples
- **Unit Tests**: `tests/test_domain/test_entities/test_artifact.py` - Domain entity testing
- **Integration Tests**: `tests/test_integration/test_api_integration.py` - API integration testing
- **Repository Tests**: `tests/test_infrastructure/test_db/repositories/test_artifact_repository.py` - Database testing
- **Use Case Tests**: `tests/test_application/test_use_cases/test_get_artifact.py` - Business logic testing

### Adding New Dependencies

Add dependencies to `pyproject.toml`:

```toml
[project]
dependencies = [
    "existing-dependency",
    "new-dependency>=1.0.0",
]
```

### Customizing Docker

Modify `docker-compose.yml` to:
- Add new services
- Change service configurations
- Adjust networking and volumes

## 🤝 Contributing

Want to contribute? Check out our [contribution guide](CONTRIBUTING.md) for guidelines.

## 📄 License

This template is available under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the powerful ORM
- [Dishka](https://github.com/reagento/dishka) for dependency injection
- [Faststream](https://github.com/ag2ai/faststream) for the convenient work with message brokers
- [Cookiecutter](https://cookiecutter.readthedocs.io/) for project templating

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the generated project's README.md

---

**Happy coding! 🚀**
