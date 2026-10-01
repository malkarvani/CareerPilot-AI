from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db


resume_builder = Blueprint(
    "resume_builder",
    __name__
)


@resume_builder.route("/resume/builder", methods=["GET", "POST"])
@login_required
def builder():

    if request.method == "POST":

        # Get information from form
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        location = request.form.get("location", "").strip()

        education = request.form.get("education", "").strip()
        skills = request.form.get("skills", "").strip()
        experience = request.form.get("experience", "").strip()
        projects = request.form.get("projects", "").strip()

        career_goal = request.form.get(
            "career_goal",
            ""
        ).strip()

        bio = request.form.get(
            "bio",
            ""
        ).strip()

        # Basic validation
        if not name:
            flash("Please enter your name.", "error")

            return redirect(
                url_for("resume_builder.builder")
            )

        if not email:
            flash("Please enter your email.", "error")

            return redirect(
                url_for("resume_builder.builder")
            )

        # Save useful information to profile
        current_user.name = name

        if hasattr(current_user, "education"):
            current_user.education = education

        if hasattr(current_user, "skills"):
            current_user.skills = skills

        if hasattr(current_user, "experience"):
            current_user.experience = experience

        if hasattr(current_user, "career_goal"):
            current_user.career_goal = career_goal

        if hasattr(current_user, "bio"):
            current_user.bio = bio

        if hasattr(current_user, "interests"):
            current_user.interests = projects

        db.session.commit()

        flash(
            "Resume information saved successfully!",
            "success"
        )

        # Show generated resume
        return render_template(
            "resume_builder.html",
            user=current_user,
            resume_data={
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "career_goal": career_goal,
                "bio": bio,
                "education": education,
                "skills": skills,
                "experience": experience,
                "projects": projects
            },
            generated=True
        )

    # GET request
    return render_template(
        "resume_builder.html",
        user=current_user,
        resume_data=None,
        generated=False
    )