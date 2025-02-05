from config import QUESTIONS_FILE
import random

# Savol qo'shish
def add_question(question):
    with open(QUESTIONS_FILE, "a", encoding="utf-8") as file:
        file.write(question.strip() + " ?\n")

# Barcha savollarni o‘chirish
def delete_all_questions():
    open(QUESTIONS_FILE, "w").close()

# Tasodifiy savollarni olish
def get_random_questions(limit=5):
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            data = file.read()
            questions = [q.strip() for q in data.split("?") if q.strip()]
            return random.sample(questions, min(len(questions), limit))
    except FileNotFoundError:
        return []
