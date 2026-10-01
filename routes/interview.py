from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from services.groq_service import generate_ai_response


interview = Blueprint(
    "interview",
    __name__
)


@interview.route("/interview", methods=["GET", "POST"])
@login_required
def home():

    questions = None

    career_goal = getattr(
        current_user,
        "career_goal",
        ""
    ) or ""

    education = getattr(
        current_user,
        "education",
        ""
    ) or ""

    skills = getattr(
        current_user,
        "skills",
        ""
    ) or ""

    experience = getattr(
        current_user,
        "experience",
        ""
    ) or ""

    interests = getattr(
        current_user,
        "interests",
        ""
    ) or ""


    if request.method == "POST":

        prompt = f"""
You are CareerAI, a professional interview coach.

Create a personalized interview preparation
session based on the user's career profile.

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


Create:

1. 5 technical interview questions
2. 5 behavioral interview questions
3. A short explanation of what the interviewer
   wants to know from each question
4. Practical interview preparation tips
5. A short final checklist

Make the questions relevant to the user's
career goal and skills.

Do not invent information about the user.
Keep the advice practical and professional.
"""

        try:

            questions = generate_ai_response(
                prompt
            )

        except Exception as e:

            print(
                "Interview Preparation Error:",
                e
            )

            questions = (
                "Sorry, interview preparation "
                "could not be generated right now. "
                "Please try again later."
            )


    return render_template(
        "interview.html",
        user=current_user,
        questions=questions
    )