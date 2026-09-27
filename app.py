from datetime import date

from flask import Flask, jsonify, request

from services.storage import DATA_FILE, load_courses, save_courses

VALID_STATUSES = {"Not Started", "In Progress", "Completed"}
REQUIRED_FIELDS = ("name", "description", "target_completion_date", "status")

app = Flask(__name__)
app.config["COURSES_FILE"] = DATA_FILE


def find_course(courses, course_id):
    return next((course for course in courses if course["id"] == course_id), None)


def validate_course(payload):
    if not isinstance(payload, dict):
        return "A JSON object is required"

    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        return f"Missing required fields: {', '.join(missing)}"

    for field in ("name", "description"):
        if not isinstance(payload[field], str) or not payload[field].strip():
            return f"{field} must be a non-empty string"

    if not isinstance(payload["status"], str) or payload["status"] not in VALID_STATUSES:
        return f"status must be one of: {', '.join(sorted(VALID_STATUSES))}"

    try:
        date.fromisoformat(payload["target_completion_date"])
    except (TypeError, ValueError):
        return "target_completion_date must use YYYY-MM-DD format"

    return None


@app.get("/api/courses")
def list_courses():
    return jsonify({"courses": load_courses(app.config["COURSES_FILE"])})


@app.post("/api/courses")
def create_course():
    payload = request.get_json(silent=True)
    error = validate_course(payload)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses(app.config["COURSES_FILE"])
    course = {"id": max((item["id"] for item in courses), default=0) + 1}
    course.update({
        field: payload[field].strip() if field in ("name", "description") else payload[field]
        for field in REQUIRED_FIELDS
    })
    courses.append(course)
    save_courses(courses, app.config["COURSES_FILE"])
    return jsonify(course), 201


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    course = find_course(load_courses(app.config["COURSES_FILE"]), course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course)


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    payload = request.get_json(silent=True)
    error = validate_course(payload)
    if error:
        return jsonify({"error": error}), 400

    courses = load_courses(app.config["COURSES_FILE"])
    course = find_course(courses, course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404

    for field in REQUIRED_FIELDS:
        course[field] = payload[field].strip() if field in ("name", "description") else payload[field]
    save_courses(courses, app.config["COURSES_FILE"])
    return jsonify(course)


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses(app.config["COURSES_FILE"])
    remaining_courses = [course for course in courses if course["id"] != course_id]
    if len(remaining_courses) == len(courses):
        return jsonify({"error": "Course not found"}), 404

    save_courses(remaining_courses, app.config["COURSES_FILE"])
    return jsonify({"message": "Course deleted"})


if __name__ == "__main__":
    app.run(debug=True)