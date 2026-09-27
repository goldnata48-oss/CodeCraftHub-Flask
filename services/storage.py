import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "courses.json"


def load_courses(file_path=DATA_FILE):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text('{\n  "courses": []\n}\n', encoding="utf-8")

    with path.open("r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    if not isinstance(data, dict) or not isinstance(data.get("courses"), list):
        raise ValueError('Courses file must contain an object with a "courses" list')
    return data["courses"]


def save_courses(courses, file_path=DATA_FILE):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as data_file:
        json.dump({"courses": courses}, data_file, ensure_ascii=False, indent=2)
        data_file.write("\n")