
import re

EXPECTED_ANSWERS = {
    "python": {
        "keywords": [
            "python", "interpreted", "high level",
            "dynamic typing", "readability", "libraries"
        ],
        "concepts": [
            "Python is a high-level programming language",
            "Python supports dynamic typing",
            "Python has a large standard library"
        ]
    },
    "oops": {
        "keywords": [
            "class", "object", "inheritance",
            "polymorphism", "encapsulation", "abstraction"
        ],
        "concepts": [
            "Classes and objects",
            "Inheritance and code reusability",
            "Polymorphism, encapsulation and abstraction"
        ]
    },
    "database": {
        "keywords": [
            "database", "table", "rows",
            "columns", "sql", "query"
        ],
        "concepts": [
            "Database stores organised data",
            "Tables contain rows and columns",
            "SQL is used to manage relational databases"
        ]
    }
}


def evaluate_answer(question, answer):
    if not answer or not answer.strip():
        return {
            "accuracy_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": ["Please submit an answer first."]
        }

    text = answer.lower()
    question_text = question.lower()

    if "oops" in question_text or "object oriented" in question_text:
        data = EXPECTED_ANSWERS["oops"]
    elif "database" in question_text or "sql" in question_text:
        data = EXPECTED_ANSWERS["database"]
    else:
        data = EXPECTED_ANSWERS["python"]

    keywords = data["keywords"]

    matched = [
        word for word in keywords
        if re.search(r"\b" + re.escape(word) + r"\b", text)
    ]

    missing = [word for word in keywords if word not in matched]

    score = round((len(matched) / len(keywords)) * 100)

    suggestions = []

    if score < 40:
        suggestions.append("Revise the basic concepts related to this question.")
    elif score < 70:
        suggestions.append("Your answer is partially correct. Add more technical details.")
    else:
        suggestions.append("Good answer! Try adding a practical example.")

    if missing:
        suggestions.append(
            "Include these missing concepts: " + ", ".join(missing)
        )

    if len(answer.split()) < 20:
        suggestions.append("Explain your answer in more detail.")

    return {
        "accuracy_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions": suggestions
    }
