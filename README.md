 
# Business Control System
Business Control System — это микросервисное приложение для управления командами, задачами, встречами и оценками сотрудников.
Архитектура построена по принципу разделения ответственности, каждая бизнес-область представлена отдельным сервисом.

## 🚀 Стек технологий

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.39-red?logo=python)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.10.6-blue?logo=pydantic)](https://docs.pydantic.dev/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.34.0-purple?logo=uvicorn)](https://www.uvicorn.org/)
[![asyncpg](https://img.shields.io/badge/asyncpg-0.30.0-orange)](https://magicstack.github.io/asyncpg/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker--Compose-enabled-1488C6?logo=docker)](https://docs.docker.com/compose/)
[![Kafka](https://img.shields.io/badge/Kafka-enabled-231F20?logo=apachekafka)](https://kafka.apache.org/)
[![httpx](https://img.shields.io/badge/httpx-0.27.0-68a063)](https://www.python-httpx.org/)

---

## 📦 Сервисы

Проект состоит из нескольких микросервисов, каждый из которых выполняет отдельную функцию:

| Сервис               | Назначение                                                                 |
|----------------------|----------------------------------------------------------------------------|
| `users_service`      | Регистрация, авторизация, управление профилем                              |
| `teams_service`      | Работа с командами и инвайт-кодами                                         |
| `org_service`        | Управление структурами и подразделениями                                   |
| `tasks_service`      | Создание и обновление задач, комментарии, статусы                         |
| `calendar_service`   | Календарь событий и задач, проверка доступности                           |
| `meeting_service`    | Создание встреч, проверка занятости                                        |
| `evaluation_service` | Оценка эффективности, формирование квартальных показателей                 |
| `api_gateway`        | Объединённый Swagger UI и точка входа                                      |

---

## 🧭 Навигация и документация

- Все микросервисы имеют `/docs` и `/openapi.json` для Swagger-документации.
- API Gateway автоматически объединяет документацию всех сервисов и отображает её по адресу:  
  👉 **`http://localhost:8010/docs`**

---

## 🐳 Запуск через Docker Compose

```bash
docker-compose up --build
```

Сервисы автоматически стартуют в своей сети, и каждый будет доступен по своему имени  внтури контейнера (например, `http://users_service:8000`).

---

## 🔐 Аутентификация

Некоторые сервисы защищены JWT-аутентификацией и требуют передачи `Authorization: Bearer <token>`.

---

## 📚 Лицензия

MIT License. Свободное использование в личных и коммерческих целях.
