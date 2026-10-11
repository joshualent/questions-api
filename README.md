# Questions API

Follow along and build a backend API where people can submit questions, vote on them, and mark them answered. The workshop progresses from an empty Django app to CRUD, custom actions, authentication and staff moderation, then many-to-many voting. Each checkpoint is a working version of the project.

## Before you start

You will need:

- Git.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage Python and dependencies.
- A text editor and a terminal.

The project uses Python 3.14. uv can install it when you run `uv sync`. The committed `uv.lock` keeps everyone on the same dependency versions.

Clone the repository:

```bash
git clone https://github.com/joshualent/questions-api.git
cd questions-api
```

## Start the workshop

`main` and `checkpoint-0-setup` both contain the prepared Django scaffold. A fresh clone starts here. To begin the workshop:

```bash
git switch main
uv sync --locked
uv run manage.py migrate
uv run manage.py runserver
```

Open <http://127.0.0.1:8000/admin/>. At this checkpoint the admin login page exists, but there is no questions API yet.

Keep the server running in one terminal and use another for commands, or stop the server with `Ctrl+C` when you need the terminal. Run commands from the directory containing `manage.py`.

If you want to create the scaffold yourself, follow [INITIAL_SETUP.md](INITIAL_SETUP.md).

## Checkpoints

Each branch contains the completed version of its lesson. The branches share one linear history, with one commit for each checkpoint.

| Branch | What is already complete | What we build next |
| --- | --- | --- |
| `checkpoint-0-setup` | Django project, dependencies and empty questions app | Basic CRUD |
| `checkpoint-1-crud` | Question model, serializer, viewset, router and admin registration | Custom actions |
| `checkpoint-2-actions` | Integer upvotes and answered toggling | Authentication and permissions |
| `checkpoint-3-auth` | Login, authenticated voting and staff moderation | Many-to-many voting |
| `checkpoint-4-m2m` | Votes track users and can be toggled | Workshop complete |
| `main` | Same starting code as `checkpoint-0-setup` | Basic CRUD |

`checkpoint-4-m2m` contains the finished project.

For example, if you fall behind before the authentication lesson, switch to `checkpoint-2-actions` so you have the completed actions code.

Before switching, stop the server. Check for local changes:

```bash
git status
```

If you have changes you want to keep, save them in a stash. `-u` also saves new files that Git is not tracking yet:

```bash
git stash push -u -m "My workshop progress"
```

Then switch to the checkpoint you need and start again:

```bash
git switch checkpoint-2-actions
uv sync --locked
uv run manage.py migrate
uv run manage.py runserver
```

Your stash stays available with `git stash list`. You can inspect it later; you do not need to apply it to continue from the checkpoint.

Git changes the code when you switch branches. It does not change the local database. Read the database instructions below if you move backward across the many-to-many lesson.

## Lesson 1: Basic CRUD

We introduce the `Question` model, its serializer, a `ModelViewSet`, and a `DefaultRouter`. Registering the model in Django admin also lets us inspect questions there.

Each question has:

| Field | Purpose |
| --- | --- |
| `id` | Automatically generated identifier |
| `text` | Question text, up to 300 characters |
| `votes` | Integer count, initially zero |
| `answered` | Boolean, initially false |
| `created_at` | Automatically recorded creation time |

Only `text` is writable through the serializer. The other fields are read-only from their first introduction.

After adding the model, generate and apply its migration:

```bash
uv run manage.py makemigrations questions
uv run manage.py migrate
```

Open <http://127.0.0.1:8000/api/questions/> to use the browsable API. These routes support CRUD:

| Method | URL | Operation |
| --- | --- | --- |
| `GET` | `/api/questions/` | List questions |
| `POST` | `/api/questions/` | Create a question |
| `GET` | `/api/questions/1/` | Read question 1 |
| `PUT` | `/api/questions/1/` | Replace its writable fields |
| `PATCH` | `/api/questions/1/` | Update its writable fields |
| `DELETE` | `/api/questions/1/` | Delete it |

Replace `1` with an ID from your own database. Keep the trailing slash on API URLs.

To create a question, send:

```json
{
  "text": "What does a serializer do?"
}
```

CRUD is public in this lesson. We restrict editing and deleting in the authentication lesson.

## Lesson 2: Custom actions

We add two detail actions to the viewset:

| Method | URL | Behavior |
| --- | --- | --- |
| `POST` | `/api/questions/1/upvote/` | Increase the integer vote count by one |
| `POST` | `/api/questions/1/toggle_answered/` | Switch answered between true and false |

Neither action needs a request body. Calling `toggle_answered` twice returns the question to its previous state. At this stage, both actions are public.

These actions only change the values stored in existing fields. The model's fields stay the same, so no migration is needed.

## Lesson 3: Authentication and staff moderation

We add browsable API login at `/api-auth/` and permissions on the viewset and its actions. Voting still increments an integer in this lesson.

| Operation | Who can do it? |
| --- | --- |
| List, read or create questions | Anyone, including logged-out visitors |
| Upvote | Any logged-in user |
| Edit or delete questions | Staff users |
| Toggle answered | Staff users |

`IsAdminUser` checks the user's **staff status**, the `is_staff` field on the user model Django provides. There is no question ownership system in this workshop.

Create a local moderator account:

```bash
uv run manage.py createsuperuser
```

Sign in at <http://127.0.0.1:8000/admin/>. A superuser is also a staff user, so this account can moderate questions.

To try the ordinary-user permissions, use the admin's Users page to create another account. Leave **Staff status** and **Superuser status** unchecked. Give it a password so it can log in.

Visit <http://127.0.0.1:8000/api/questions/> and use the browsable API's **Log in** link. Compare what you can do while logged out, logged in as the ordinary user, and logged in as the moderator. Django admin and the browsable API share the browser's login session.

For logged-in requests, the browsable API handles the session and CSRF token for you.

## Lesson 4: Many-to-many voting

We replace the integer field with a many-to-many relationship to Django's user model. A question now remembers which users voted for it.

The serializer still returns `votes` as a read-only integer count. It also adds a read-only `has_voted` boolean indicating whether the requesting user has voted for the question. Logged-out visitors receive `false`.

The voting action changes:

| Method | URL | Behavior |
| --- | --- | --- |
| `POST` | `/api/questions/1/toggle_vote/` | Add your vote if absent; remove it if present |

`/upvote/` is removed in this checkpoint. `/toggle_answered/` and the permission rules stay the same.

Each user can contribute at most one vote to a question. Try voting with two accounts, then removing one account's vote: the other user's vote remains.

Generate and apply the migration:

```bash
uv run manage.py makemigrations questions --name votes_many_to_many
uv run manage.py migrate
```

If you switched to a completed checkpoint instead of writing the code, its migration is already committed. Run `migrate`; you do not need to generate it again.

## Databases and branch changes

The SQLite database, `db.sqlite3`, is local and ignored by Git. Switching branches or stashing code does not reset it.

When moving forward, run `uv run manage.py migrate` after switching. The many-to-many migration preserves questions and user accounts, but resets votes: old totals cannot tell us which users voted.

To move backward from the many-to-many code while keeping questions and accounts, reverse that migration **before switching branches**:

```bash
# Run this while still on checkpoint-4-m2m.
uv run manage.py migrate questions 0001

git switch checkpoint-3-auth
uv run manage.py migrate
```

The integer vote counts return to zero. Reversing the migration cannot recover the previous totals.

If you have already switched to an earlier checkpoint, save any code changes and return to `checkpoint-4-m2m` before running the reversal. For a fresh start at any checkpoint, stop the server, delete the disposable `db.sqlite3` file, then run `migrate` again. This deletes all local questions and accounts; recreate your moderator account with `createsuperuser` when needed.

In production, schema changes need migrations and a deliberate plan for preserving data. This workshop uses a disposable development database and intentionally discards old vote totals during the refactor.
