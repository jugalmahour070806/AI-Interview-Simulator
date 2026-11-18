
import random

# ---------------- QUESTION BANK ----------------

questions = {
    "Python Developer": [
        "What is the difference between a list and a tuple in Python?",
        "Explain the concept of inheritance in Python.",
        "What is exception handling and why is it used?"
    ],
    "Web Developer": [
        "What is the difference between HTML, CSS and JavaScript?",
        "What is the difference between GET and POST requests?",
        "What is responsive web design?"
    ],
    "Data Analyst": [
        "What is the difference between mean and median?",
        "What is data cleaning and why is it important?",
        "What is the purpose of SQL GROUP BY?"
    ],
    "Cybersecurity": [
        "What is the difference between encryption and hashing?",
        "What is phishing and how can it be prevented?",
        "What is the principle of least privilege?"
    ]
}

# ---------------- ANSWER KEYWORDS ----------------

keywords = {
    "Python Developer": [
        ["mutable", "immutable", "change", "tuple", "ordered"],
        ["class", "parent", "child", "inherit", "reuse"],
        ["try", "except", "error", "exception", "handle"]
    ],
    "Web Developer": [
        ["html", "structure", "css", "style", "javascript", "behavior"],
        ["get", "retrieve", "post", "send", "data", "server"],
        ["responsive", "screen", "device", "media query", "layout"]
    ],
    "Data Analyst": [
        ["mean", "average", "median", "middle", "outlier"],
        ["clean", "missing", "duplicate", "incorrect", "quality"],
        ["group", "aggregate", "category", "count", "sum"]
    ],
    "Cybersecurity": [
        ["encryption", "key", "decrypt", "hash", "one-way"],
        ["phishing", "fake", "email", "link", "verify"],
        ["least privilege", "minimum", "permission", "access", "role"]
    ]
}

# ---------------- INTERVIEWER FUNCTIONS ----------------

def get_interview_question(question_list):
    if not question_list:
        return "No questions available."
    return random.choice(question_list)

def get_feedback_message():
    messages = [
        "Thank you for your answer. Let's move to the next question.",
        "Good effort. Let's continue.",
        "Thank you. Let's proceed to the next question."
    ]
    return random.choice(messages)
