# Тестовое задание Nebus

Приложение предназначено для выдачи данных по организациям (read-only).

## Запуск

1. **Скопируйте файл конфигурации:**
    ```bash
    cp .env.temp .env
    ```
2. **Заполните переменные окружения в файле `.env`** необходимыми значениями (например, учетные данные HH.ru, настройки поиска и текста отклика).
3. **Запустите бота с помощью Docker Compose:**
    ```bash
    docker compose up -d --build
    ```
   Или с помощью Podman Compose:
    ```bash
    podman-compose up -d --build
    ```

## Использование собственной базы данных PostgreSQL

По умолчанию предполагается использование внешней БД PostgreSQL. Если хотите развернуть PostgreSQL в контейнере, добавьте сервис в `docker-compose.yml`:
    ```yaml
    postgres:
        image: postgres:17
        container_name: test_secrets_postgres
        env_file:
          - .env
        volumes:
          - postgres_data:/var/lib/postgresql/data
        restart: unless-stopped
    ```
   И определите volume:
    ```yaml
    volumes:
      postgres_data:
    ```
   Добавьте зависимость в сервис 'app':
    ```yaml
    depends_on:
      - postgres
    ```
   
## Примечания

- Ключ авторизации статичен и передаётся в заголовке `X-API-KEY`.

## Автор

[Telegram: @two_percent](https://t.me/two_percent)