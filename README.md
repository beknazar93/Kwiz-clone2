# Kwiz Clone Backend

Бэкенд-клонирование приложения Kwiz, разработанное с использованием Django.

## ⚙️ Стек технологий

- Python
- Django

## 🚀 Начало работы

### 1. Клонирование репозитория

```bash
git clone https://github.com/beknazar93/Kwiz-clone2.git
2. Установка зависимостей
Перейдите в директорию проекта и создайте виртуальное окружение:

bash
Копировать
Редактировать
cd Kwiz-clone2
python -m venv env
Активируйте виртуальное окружение:

Для Windows:

bash
Копировать
Редактировать
.\env\Scripts\activate
Для Unix или MacOS:

bash
Копировать
Редактировать
source env/bin/activate
Установите необходимые пакеты:

bash
Копировать
Редактировать
pip install -r requirements.txt
3. Применение миграций и запуск сервера разработки
Примените миграции базы данных:

bash
Копировать
Редактировать
python manage.py migrate
Запустите сервер разработки:

bash
Копировать
Редактировать
python manage.py runserver
После запуска откройте браузер и перейдите по адресу http://127.0.0.1:8000/.

📁 Структура проекта
bash
Копировать
Редактировать
Kwiz-clone2/
├── api/                # Приложение Django для API
├── myproject/          # Основные настройки проекта Django
├── db.sqlite3          # Файл базы данных SQLite
├── manage.py           # Управляющий скрипт Django
├── requirements.txt    # Список зависимостей проекта
└── Procfile            # Файл для развертывания на Heroku
