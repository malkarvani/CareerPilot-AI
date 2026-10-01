from flask import Blueprint, render_template, request
from flask_login import login_required, current_user


portfolio = Blueprint("portfolio", __name__)


@portfolio.route("/portfolio", methods=["GET", "POST"])
@login_required
def home():

    portfolio_data = {
        "name": getattr(current_user, "name", "") or "",
        "career_goal": getattr(current_user, "career_goal", "") or "",
        "education": getattr(current_user, "education", "") or "",
        "skills": getattr(current_user, "skills", "") or "",
        "experience": getattr(current_user, "experience", "") or "",
        "interests": getattr(current_user, "interests", "") or "",
        "projects": ""
    }

    if request.method == "POST":

        portfolio_data["projects"] = request.form.get(
            "projects",
            ""
        ).strip()

    return render_template(
        "portfolio.html",
        user=current_user,
        portfolio=portfolio_data
    )