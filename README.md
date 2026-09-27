# CodeCraftHub API

A small Flask REST API for tracking courses. Course data is stored in `data/courses.json`.

## Run locally

```powershell
cd CodeCraftHub-Flask
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

The API runs at `http://127.0.0.1:5000`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/courses` | List all courses |
| `POST` | `/api/courses` | Create a course |
| `GET` | `/api/courses/<course_id>` | Get one course |
| `PUT` | `/api/courses/<course_id>` | Replace a course (all fields required) |
| `DELETE` | `/api/courses/<course_id>` | Delete a course |

A course requires `name`, `description`, `target_completion_date` (`YYYY-MM-DD`), and `status`. Allowed statuses are `Not Started`, `In Progress`, and `Completed`.

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/courses `
  -H "Content-Type: application/json" `
  -d '{"name":"Python for Beginners","description":"Learn Python basics","target_completion_date":"2026-10-15","status":"In Progress"}'
```

## GitHub

Initialize Git from this directory so the older project in the parent directory is not included:

```powershell
git init
git add .
git commit -m "Add CodeCraftHub Flask API"
```