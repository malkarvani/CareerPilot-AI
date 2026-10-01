from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db


profile = Blueprint(
    "profile",
    __name__
)


@profile.route("/profile", methods=["GET", "POST"])
@login_required
def home():

    if request.method == "POST":

        current_user.name = request.form.get(
            "name",
            ""
        ).strip()

        current_user.education = request.form.get(
            "education",
            ""
        ).strip()

        current_user.skills = request.form.get(
            "skills",
            ""
        ).strip()

        current_user.experience = request.form.get(
            "experience",
            ""
        ).strip()

        current_user.interests = request.form.get(
            "interests",
            ""
        ).strip()

        current_user.career_goal = request.form.get(
            "career_goal",
            ""
        ).strip()

        current_user.bio = request.form.get(
            "bio",
            ""
        ).strip()


        db.session.commit()


        flash(
            "Profile updated successfully!",
            "success"
        )


        return redirect(
            url_for("profile.home")
        )


    return render_template(
        "profile.html",
        user=current_user
    )