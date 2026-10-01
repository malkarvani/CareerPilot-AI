from flask import Blueprint, render_template
from flask_login import login_required, current_user

from services.groq_service import generate_ai_response


certifications = Blueprint(
    "certifications",
    __name__
)


@certifications.route("/certifications")
@login_required
def home():

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


    prompt = f"""
You are CareerAI, a professional career advisor.

Recommend professional certifications that are
relevant to the user's career profile.

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


Give 5 useful certification recommendations.

For each certification include:

1. Certification name
2. Issuing organization
3. Why it is recommended
4. Skills covered
5. Difficulty level
6. Career benefit

Important:

- Personalize recommendations to the user's profile.
- Do not invent information about the user.
- Prefer well-known and relevant certifications.
- Keep the recommendations practical.
- Clearly explain why each certification is useful.
"""


    recommendations = None

    try:

        recommendations = generate_ai_response(
            prompt
        )

    except Exception as e:

        print(
            "Certification Recommendation Error:",
            e
        )

        recommendations = (
            "Sorry, certification recommendations "
            "could not be generated right now. "
            "Please try again later."
        )


    return render_template(
        "certifications.html",
        user=current_user,
        recommendations=recommendations
    )