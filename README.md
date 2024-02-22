Тестовое задание к собеседованию.

Что применял: SQLAlchemy, alembic, pydantic-settings

## Запуск приложения

**1. Копируем репозиторий, создаем виртуальное окружение и устанавливаем poetry**

    pip install poetry && poetry config virtualenvs.create false

**2. Устанавливаем зависимости:**
    
    poetry install --no-dev

**3. Поднять базу данных postgres, для этогого в файле ".env" необходимо
ввести свои данные.**

После чего поднимаем контейнер с БД в фоновом режиме:

    docker compose up -d

**4. Прогоняем миграции:**

    alembic upgrade head

**5. Задание не подразумевало написание кода для вставки данных, поэтому делаем это сами))**

**6. Запускаем main.py и видим требуемый по ТЗ вывод.**
