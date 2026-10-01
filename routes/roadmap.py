from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from services.groq_service import generate_career_roadmap


roadmap = Blueprint(
    "roadmap",
    __name__,
    url_prefix="/roadmap"
)


@roadmap.route("/", methods=["GET", "POST"])
@login_required
def home():

    roadmap_result = None
    error = None

    if request.method == "POST":

        # --------------------------------------------------
        # GET FORM DATA
        # --------------------------------------------------

        career_goal = request.form.get(
            "career_goal",
            ""
        ).strip()

        current_level = request.form.get(
            "current_level",
            "Beginner"
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        # Optional fields for compatibility with older forms
        experience = request.form.get(
            "experience",
            ""
        ).strip()

        interests = request.form.get(
            "interests",
            ""
        ).strip()

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not career_goal:

            error = "Please enter your career goal."

        else:

            # Use sensible defaults
            if not current_level:
                current_level = "Beginner"

            if not education:
                education = "Not specified"

            if not skills:
                skills = "Not specified"

            if not experience:
                experience = "Not specified"

            if not interests:
                interests = "Not specified"

            # --------------------------------------------------
            # GENERATE AI ROADMAP
            # --------------------------------------------------

            try:

                roadmap_result = generate_career_roadmap(
                    career_goal=career_goal,
                    current_level=current_level,
                    education=education,
                    experience=experience,
                    skills=skills,
                    additional_info=interests
                )

            except Exception as e:

                error = (
                    "Unable to generate your roadmap right now. "
                    f"{str(e)}"
                )

    # ------------------------------------------------------
    # RENDER PAGE
    # ------------------------------------------------------

    return render_template(
        "roadmap.html",
        roadmap_result=roadmap_result,
        error=error,
        user=current_user
    )