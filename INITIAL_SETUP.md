# Initial repository setup

These are the steps that created this starter repository. Follow them if you'd rather start from scratch than clone the repo.

1. Initialize the project

```bash
uv init --python 3.14 --name questions-api
uv add "django~=6.1.0" "djangorestframework~=3.18.0"
uv run django-admin startproject config .
```

This creates a Django project with its settings and other configuration in the `config` directory. `uv init` creates a `main.py` file that django doesn't use, it's safe to delete it.

Add `db.sqlite3` to the end of the `.gitignore` file. This tells git not to track the database file.

```conf
.venv

# new
db.sqlite3
```

2. Set up Django REST Framework and the questions app

Django calls each part of a project an "app". Apps make it easy to move functionality from one project to another, and third-party packages like djangorestframework are apps too.

```bash
uv run manage.py startapp questions
```

Add the new `questions` app AND `rest_framework` to `INSTALLED_APPS` in `config/settings.py`. This tells Django to use the app we just created and the djangorestframework package we added.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'questions', # new
    'rest_framework', # new
]
```

Finally, you'll need to create a file called `serializers.py` in the `questions` directory.

```bash
questions
├── admin.py
├── apps.py
├── __init__.py
├── migrations
├── models.py
├── serializers.py # new
├── tests.py
└── views.py
```
