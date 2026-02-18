# Blogicum

Blogicum — учебный Django-проект блога с публикациями, категориями и локациями.  
Проект реализует отображение только опубликованного контента с учётом даты публикации и статуса категории.

## Технологии

- Python 3.12
- Django 5.1
- SQLite
- Pytest + pytest-django
- Mixer (фикстуры для тестов)

## Установка и запуск

1. Клонировать репозиторий:

```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd django-sprint3-main
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Применить миграции:

```bash
cd blogicum
python manage.py makemigrations
python manage.py migrate
```

5. Загрузить фикстуры:

```bash
python manage.py loaddata ../db.json
```

6. Запустить сервер:

```bash
python manage.py runserver
```

## Запуск тестов

Из корня проекта:

```bash
python -m pytest
```

## Структура проекта

```text
django-sprint3-main/
├── blogicum/
│   ├── blog/                # Модели, вью, URL и админка блога
│   ├── pages/               # Статические страницы /pages/about/ и /pages/rules/
│   ├── blogicum/            # Настройки проекта, корневые URL, шаблоны
│   └── manage.py
├── templates/               # Шаблоны sprint 3 (источник)
├── tests/                   # Тесты проекта
├── db.json                  # Фикстуры
└── requirements.txt
```

## Модели

### `Category`
- `title` — заголовок категории.
- `description` — описание категории.
- `slug` — уникальный slug для URL.
- `is_published` — флаг публикации категории.
- `created_at` — дата создания.

### `Location`
- `name` — название места.
- `is_published` — флаг публикации локации.
- `created_at` — дата создания.

### `Post`
- `title` — заголовок публикации.
- `text` — текст публикации.
- `pub_date` — дата/время публикации.
- `author` — автор (через `get_user_model()`).
- `location` — опциональная локация (`SET_NULL`).
- `category` — категория поста.
- `is_published` — флаг публикации поста.
- `created_at` — дата создания.

## Логика отображения публикаций

- Главная страница: показывает 5 последних постов, где:
  - `post.is_published = True`
  - `post.pub_date <= now`
  - `post.category.is_published = True`
- Страница категории:
  - если категория не опубликована, возвращается `404`;
  - иначе выводятся посты этой категории с теми же ограничениями по публикации/дате.
- Страница поста:
  - `404`, если пост не опубликован, дата публикации в будущем или категория снята с публикации.
- Статус публикации локации не влияет на доступность поста.
- Для оптимизации запросов используется `select_related`.

## Автор

- Александр Пивоваров
