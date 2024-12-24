# MyData: Платформа для анализа больших объёмов данных

**MyData** — это веб-приложение, предназначенное для работы с большими объёмами данных. Платформа позволяет загружать данные, фильтровать их, визуализировать и создавать интерактивные дашборды.

## Стек технологий

Для разработки платформы использовались следующие технологии и инструменты:

- **Python** — основной язык программирования.
- **Django** — веб-фреймворк для разработки серверной части.
- **PostgreSQL** — система управления базами данных.
- **Plotly/Dash** — библиотека для построения интерактивных графиков и интеграции с Django.
- **Pandas** и **PyArrow** — для обработки данных и сохранения их в формате Parquet.
- **HTML, CSS** — для реализации пользовательского интерфейса.

## Структура проекта

Проект был реализован с использованием фреймворка Django, который предоставляет удобные инструменты для разработки веб-приложений, включая обработку запросов, маршрутизацию, работу с базой данных и интеграцию с фронтенд-частью. Основная цель заключалась в создании платформы для анализа данных файлов, построения интерактивных графиков и создания дашбордов.

### Архитектура проекта

Приложение состоит из пяти модулей:

1. **files** — отвечает за загрузку и обработку файлов:
   - Реализован функционал предобработки файлов.
   - Загрузка файлов в формате CSV с последующим сохранением в формате Parquet для повышения эффективности работы с большими данными.

2. **charts** — реализует функциональность построения графиков и работы с визуализацией данных:
   - Построение интерактивных графиков с использованием Plotly.
   - Сохранение параметров графиков в формате JSON для последующего восстановления.
   - Возможность экспорта графиков в формате PNG.

3. **dashboards** — управляет созданием и отображением дашбордов:
   - Объединение нескольких графиков в интерактивные дашборды.
   - Настройка отображения графиков на дашборде.

4. **registrations** — отвечает за регистрацию, авторизацию и управление пользователями:
   - Использует встроенные возможности Django для обеспечения безопасности и управления сеансами.

5. **main** — предоставляет общие настройки и базовую функциональность для пользователей:
   - Подключение базы данных PostgreSQL.
   - Настройка статических и медиа-файлов.

Каждое приложение реализует отдельную часть логики, что обеспечивает удобство разработки и поддержку модульной архитектуры.

### Особенности реализации

- Для загрузки и обработки данных из файлов используются библиотеки **Pandas** и **PyArrow**, что позволяет эффективно обрабатывать большие файлы и сохранять их в формате Parquet.
- Графики поддерживают интерактивное изменение типа диаграммы и столбцов для построения в реальном времени благодаря интеграции **django_plotly_dash**.
- Все параметры графиков (название, оси, тип и т.д.) сохраняются в базе данных в формате JSON для дальнейшего использования в дашбордах.

Разработка выполнена с акцентом на простоту использования и возможность дальнейшего масштабирования платформы.

## Установка и запуск

### 1. Клонирование репозитория
Склонируйте репозиторий проекта и перейдите в его папку:
```
git clone https://github.com/username/repository.git
cd repository
```
### 2. Настройка виртуального окружения
Создайте виртуальное окружение и активируйте его:

На Windows:

```
python -m venv venv
venv\Scripts\activate
```
На macOS и Linux:

```
python3 -m venv venv
source venv/bin/activate
```
Установите зависимости:

```
pip install -r requirements.txt
```
### 3. Настройка базы данных
Откройте файл my_data/my_data/settings.py и выполните следующие действия:

- Закомментируйте строки, связанные с настройкой базы данных PostgreSQL.
- Раскомментируйте строки, связанные с настройкой SQLite либо настройте для подключения свою БД
### 4. Применение миграций
Подготовьте базу данных с помощью следующих команд:

```
python manage.py makemigrations
python manage.py migrate
```
### 5. Запуск сервера
Запустите сервер разработки:

```
python manage.py runserver
```
Откройте в браузере адрес http://127.0.0.1:8000/, чтобы начать работу с приложением.

Теперь MyData готова к использованию!
