# Pomodoro Timer (CLI + REST API)

Небольшой pet-project помодоро-таймера:

- есть **=CLI-таймер**, который считает сессии;
- каждая сессия сохраняется в **PostgreSQL**;
- поверх этого сделан **REST API на FastAPI**;
- всё упаковано в **Docker + docker-compose**;
- Написаны **юнит-тесты (pytest)**.
- Также в логике таймера задействована **многопоточность**

Проект делался как учебный, чтобы потренироваться в Python, SQLAlchemy, REST API, PostgreSQL, Docker и тестировании.

---

## Стек технологий

- Python 3.10
- FastAPI
- PostgreSQL 16
- SQLAlchemy
- Pytest
- Docker, Docker Compose
- WSL2 (под Windows)

---

## Как запустить

### Вариант 1 — через Docker (рекомендуется)

Требуется установленный Docker / Docker Desktop.


# из корня проекта
docker compose up --build
