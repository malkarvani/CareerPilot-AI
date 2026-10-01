from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from urllib.parse import quote_plus


job = Blueprint(
    "job",
    __name__
)


@job.route("/jobs", methods=["GET", "POST"])
@login_required
def finder():

    keyword = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

    # If user did not enter anything,
    # use their skills as the default search.
    if not keyword:
        keyword = getattr(current_user, "skills", "") or "software developer"

    search_keyword = quote_plus(keyword)

    jobs = [
        {
            "title": f"{keyword} Developer",
            "company": "Example Technology",
            "location": "Remote",
            "type": "Full Time",
            "description": (
                f"Looking for a motivated {keyword} "
                "professional to join our team."
            ),
            "url": f"https://www.google.com/search?q={search_keyword}+jobs"
        },
        {
            "title": f"Junior {keyword} Developer",
            "company": "Digital Solutions",
            "location": "Hybrid",
            "type": "Full Time",
            "description": (
                f"Entry-level opportunity for candidates "
                f"with {keyword} skills."
            ),
            "url": f"https://www.google.com/search?q={search_keyword}+jobs"
        },
        {
            "title": f"{keyword} Engineer",
            "company": "Innovation Labs",
            "location": "Remote",
            "type": "Full Time",
            "description": (
                f"Build and maintain applications using "
                f"{keyword} technologies."
            ),
            "url": f"https://www.google.com/search?q={search_keyword}+jobs"
        }
    ]

    return render_template(
        "jobs.html",
        jobs=jobs,
        keyword=keyword,
        user=current_user
    )