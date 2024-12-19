from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS library

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

data = {
    grade: {
        "maths": [
            {"name": "Advanced Mathematics", "publisher": "EduPub", "cost": 15.99},
            {"name": "Math for Beginners", "publisher": "LearnWell", "cost": 12.50},
        ],
        "english": [
            {"name": "Mastering English", "publisher": "LangBooks", "cost": 14.75},
            {"name": "English Essentials", "publisher": "EduReads", "cost": 10.99},
        ],
        "swahili": [
            {"name": "Kiswahili Sanifu", "publisher": "Swahili Press", "cost": 11.50},
            {"name": "Jifunze Kiswahili", "publisher": "Kisomo Ltd.", "cost": 13.20},
        ],
        "science": [
            {"name": "Exploring Science", "publisher": "ScienceWorks", "cost": 18.00},
            {"name": "Basic Physics", "publisher": "KnowledgeHub", "cost": 17.25},
        ],
        "social studies": [
            {"name": "World Around Us", "publisher": "GeoPress", "cost": 16.50},
            {"name": "History Basics", "publisher": "HistoriCo", "cost": 12.30},
        ],
        "religious education": [
            {"name": "Faith and Morals", "publisher": "SoulPrint", "cost": 9.75},
            {"name": "Religious Insights", "publisher": "BrightFaith", "cost": 10.50},
        ],
        "agriculture": [
            {"name": "Farming Basics", "publisher": "AgriBooks", "cost": 13.50},
            {"name": "Modern Agriculture", "publisher": "AgriTech", "cost": 14.80},
        ],
        "creative arts and sports": [
            {"name": "Artistic Expression", "publisher": "CreatePress", "cost": 20.00},
            {"name": "Sports Techniques", "publisher": "SportyBooks", "cost": 19.99},
        ],
        "pre-technical studies": [
            {"name": "Introduction to Tech", "publisher": "TechEd", "cost": 21.50},
            {"name": "Technical Skills", "publisher": "SkillUp", "cost": 22.30},
        ],
    }
    for grade in range(1, 10)
}

@app.route("/api/grades", methods=["GET"])
def get_grades():
    return jsonify({"grades": list(data.keys())})

@app.route("/api/grades/<int:grade>", methods=["GET"])
def get_grade_details(grade):
    if grade in data:
        return jsonify({"grade": grade, "subjects": data[grade]})
    else:
        return jsonify({"error": "Grade not found"}), 404

@app.route("/api/grades/<int:grade>/<subject>", methods=["GET"])
def get_subject_books(grade, subject):
    if grade in data and subject in data[grade]:
        return jsonify({"grade": grade, "subject": subject, "books": data[grade][subject]})
    else:
        return jsonify({"error": "Subject or grade not found"}), 404

@app.route("/api/search", methods=["GET"])
def search_book():
    book_name = request.args.get("name", "").lower()
    grade = request.args.get("grade", None)
    subject = request.args.get("subject", "").lower()
    sort_by = request.args.get("sort_by", None)
    reverse = request.args.get("order", "asc") == "desc"

    if not book_name:
        return jsonify({"error": "Please provide a book name to search."}), 400

    results = []
    for gr, subjects in data.items():
        if grade and str(gr) != str(grade):
            continue
        for sub, books in subjects.items():
            if subject and subject != sub:
                continue
            for book in books:
                if book_name in book["name"].lower():
                    results.append({
                        "grade": gr,
                        "subject": sub,
                        "book": book
                    })

    if sort_by in ["name", "publisher", "cost"]:
        results.sort(key=lambda x: x["book"][sort_by], reverse=reverse)

    if results:
        return jsonify({"results": results})
    else:
        return jsonify({"message": "No books found with the given criteria."}), 404

if __name__ == "__main__":
    app.run(debug=True)
