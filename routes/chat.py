from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from services.groq_service import generate_ai_response


chat = Blueprint("chat", __name__)


@chat.route("/chat", methods=["GET", "POST"])
@login_required
def home():

    answer = None
    question = ""

    if request.method == "POST":

        question = request.form.get("question", "").strip()

        if not question:

            answer = "Please enter a question."

        else:

            career_goal = getattr(current_user, "career_goal", "") or ""
            education = getattr(current_user, "education", "") or ""
            skills = getattr(current_user, "skills", "") or ""
            experience = getattr(current_user, "experience", "") or ""
            interests = getattr(current_user, "interests", "") or ""

            prompt = f"""
You are CareerAI, a professional AI career advisor.

USER PROFILE:

Career Goal:
{career_goal}

Education:
{education}

Skills:
{skills}

Experience:
{experience}

Interests:
{interests}

USER QUESTION:
{question}

Give clear, practical and personalized career advice.
Use bullet points when useful.
Do not invent missing profile information.
"""

            try:

                answer = generate_ai_response(prompt)

            except Exception as e:

                print("Career Chat Error:", e)

                answer = (
                    "Sorry, I could not answer your question right now. "
                    "Please try again."
                )

    return render_template(
        "chat.html",
        user=current_user,
        question=question,
        answer=answer
    )