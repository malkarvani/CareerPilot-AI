from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

import os
import uuid

from PyPDF2 import PdfReader

from services.groq_service import analyze_resume


# ============================================================
# BLUEPRINT
# ============================================================

resume = Blueprint("resume", __name__)


# ============================================================
# SETTINGS
# ============================================================

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
MAX_RESUME_TEXT_LENGTH = 50000


# ============================================================
# FILE VALIDATION
# ============================================================

def allowed_file(filename):
    return (
        bool(filename)
        and "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ============================================================
# SCORE CATEGORY
# ============================================================

def get_score_category(score):
    """
    < 40       = Poor
    40 - 74    = Average
    75 - 90    = Good
    > 90       = Excellent
    """

    try:
        score = float(score)
    except (TypeError, ValueError):
        return "Not Available"

    if score < 40:
        return "Poor"

    if score < 75:
        return "Average"

    if score <= 90:
        return "Good"

    return "Excellent"


# ============================================================
# SAFE SCORE
# ============================================================

def safe_score(value, default=0):
    try:
        value = int(float(value))
    except (TypeError, ValueError):
        value = default

    return max(0, min(100, value))


# ============================================================
# NORMALIZE LIST
# ============================================================

def normalize_list(value):
    if not value:
        return []

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str):
        return [
            line.strip()
            for line in value.splitlines()
            if line.strip()
        ]

    return []


# ============================================================
# NORMALIZE CAREER SUGGESTIONS
# ============================================================

def normalize_career_suggestions(value):
    if not isinstance(value, list):
        return []

    suggestions = []

    for item in value:

        if isinstance(item, dict):

            career = str(
                item.get("career", "")
            ).strip()

            reason = str(
                item.get("reason", "")
            ).strip()

            if career:
                suggestions.append({
                    "career": career,
                    "reason": reason
                })

        elif isinstance(item, str):

            item = item.strip()

            if item:
                suggestions.append({
                    "career": item,
                    "reason": ""
                })

    return suggestions


# ============================================================
# PREPARE AI RESULT
# ============================================================

def prepare_resume_data(data):
    """
    Make sure every value coming from Groq is safe and
    usable by the template.
    """

    if not isinstance(data, dict):
        raise ValueError(
            "Resume AI returned invalid data."
        )

    overall_score = safe_score(
        data.get("overall_score")
    )

    result = {
        "overall_score": overall_score,

        "category": get_score_category(
            overall_score
        ),

        "ats_readability": safe_score(
            data.get("ats_readability")
        ),

        "experience_fit": safe_score(
            data.get("experience_fit")
        ),

        "content_quality": safe_score(
            data.get("content_quality")
        ),

        "job_match": safe_score(
            data.get("job_match")
        ),

        "skill_alignment": safe_score(
            data.get("skill_alignment")
        ),

        "formatting": safe_score(
            data.get("formatting")
        ),

        "strengths": normalize_list(
            data.get("strengths")
        ),

        "improvements": normalize_list(
            data.get("improvements")
        ),

        "skills": normalize_list(
            data.get("skills")
        ),

        "ats_improvements": normalize_list(
            data.get("ats_improvements")
        ),

        "career_suggestions":
            normalize_career_suggestions(
                data.get("career_suggestions")
            ),

        "summary": str(
            data.get("summary", "")
        ).strip()
    }

    return result


# ============================================================
# PAGE DATA
# ============================================================

def render_resume_page(resume_data=None):
    """
    Render Resume Analyzer with all structured values.
    """

    if resume_data is None:
        resume_data = {}

    return render_template(
        "resume.html",

        # ----------------------------------------------------
        # Main data object
        # ----------------------------------------------------

        resume_data=resume_data,

        # ----------------------------------------------------
        # Overall score
        # ----------------------------------------------------

        resume_score=resume_data.get(
            "overall_score"
        ),

        score_category=resume_data.get(
            "category"
        ),

        # ----------------------------------------------------
        # Performance metrics
        # ----------------------------------------------------

        ats_readability=resume_data.get(
            "ats_readability"
        ),

        experience_fit=resume_data.get(
            "experience_fit"
        ),

        content_quality=resume_data.get(
            "content_quality"
        ),

        job_match=resume_data.get(
            "job_match"
        ),

        skill_alignment=resume_data.get(
            "skill_alignment"
        ),

        formatting=resume_data.get(
            "formatting"
        ),

        # ----------------------------------------------------
        # Resume sections
        # ----------------------------------------------------

        strengths=resume_data.get(
            "strengths",
            []
        ),

        improvements=resume_data.get(
            "improvements",
            []
        ),

        skills=resume_data.get(
            "skills",
            []
        ),

        ats_improvements=resume_data.get(
            "ats_improvements",
            []
        ),

        career_suggestions=resume_data.get(
            "career_suggestions",
            []
        ),

        summary=resume_data.get(
            "summary",
            ""
        ),

        # ----------------------------------------------------
        # Compatibility with old template
        # ----------------------------------------------------

        analysis=session.get(
            "resume_analysis"
        ),

        user=current_user
    )


# ============================================================
# RESUME ANALYZER
# ============================================================

@resume.route(
    "/resume",
    methods=["GET", "POST"]
)
@login_required
def analyzer():

    # ========================================================
    # GET
    # ========================================================

    if request.method == "GET":

        saved_data = session.get(
            "resume_analysis_data"
        )

        if not isinstance(
            saved_data,
            dict
        ):
            saved_data = {}

        return render_resume_page(
            saved_data
        )

    # ========================================================
    # POST
    # ========================================================

    print()
    print("=" * 60)
    print("CAREERAI RESUME ANALYZER")
    print("=" * 60)

    # ========================================================
    # CHECK FILE FIELD
    # ========================================================

    if "resume" not in request.files:

        flash(
            "Please select a resume PDF.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    file = request.files["resume"]

    print(
        "Uploaded file:",
        file.filename
    )

    # ========================================================
    # EMPTY FILE
    # ========================================================

    if not file.filename:

        flash(
            "Please select a resume PDF.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # PDF ONLY
    # ========================================================

    if not allowed_file(
        file.filename
    ):

        flash(
            "Only PDF files are allowed.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # SAVE PDF
    # ========================================================

    filepath = None

    try:

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        original_name = secure_filename(
            file.filename
        )

        name_without_extension = os.path.splitext(
            original_name
        )[0]

        filename = (
            f"{name_without_extension}_"
            f"{uuid.uuid4().hex[:10]}.pdf"
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(
            filepath
        )

        print(
            "PDF saved:",
            filepath
        )

    except Exception as error:

        print(
            "FILE SAVE ERROR:",
            repr(error)
        )

        flash(
            "Could not save your resume.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # READ PDF
    # ========================================================

    try:

        print(
            "Extracting PDF text..."
        )

        reader = PdfReader(
            filepath
        )

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            print(
                f"Reading page {page_number}"
            )

            try:
                text = page.extract_text()
            except Exception as page_error:
                print(
                    "Page extraction error:",
                    repr(page_error)
                )
                text = None

            if text:
                pages.append(
                    text
                )

        resume_text = "\n".join(
            pages
        ).strip()

        print(
            "Extracted characters:",
            len(resume_text)
        )

    except Exception as error:

        print(
            "PDF EXTRACTION ERROR:",
            repr(error)
        )

        flash(
            "Could not read this PDF. "
            "Please upload a valid text-based PDF.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # NO TEXT
    # ========================================================

    if not resume_text:

        flash(
            "Could not extract text from this PDF. "
            "Please upload a text-based PDF instead of "
            "a scanned image PDF.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # LIMIT TEXT
    # ========================================================

    if len(resume_text) > MAX_RESUME_TEXT_LENGTH:

        resume_text = resume_text[
            :MAX_RESUME_TEXT_LENGTH
        ]

        print(
            "Resume text limited to",
            MAX_RESUME_TEXT_LENGTH,
            "characters."
        )

    # ========================================================
    # AI ANALYSIS
    # ========================================================

    try:

        print()
        print(
            "Sending resume to Groq..."
        )

        ai_result = analyze_resume(
            resume_text
        )

        print(
            "Groq response received."
        )

        print(
            "AI result type:",
            type(ai_result).__name__
        )

    except Exception as error:

        print()
        print("=" * 60)
        print("GROQ RESUME ANALYSIS ERROR")
        print("=" * 60)

        print(
            "Error type:",
            type(error).__name__
        )

        print(
            "Error:",
            repr(error)
        )

        print("=" * 60)

        flash(
            "The resume was read successfully, "
            "but AI analysis failed. "
            "Please check your GROQ_API_KEY and "
            "Groq configuration.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # PREPARE DATA
    # ========================================================

    try:

        resume_data = prepare_resume_data(
            ai_result
        )

    except Exception as error:

        print(
            "DATA PREPARATION ERROR:",
            repr(error)
        )

        flash(
            "The AI returned an unexpected resume format. "
            "Please try uploading the resume again.",
            "error"
        )

        return redirect(
            url_for("resume.analyzer")
        )

    # ========================================================
    # PRINT RESULT FOR DEBUGGING
    # ========================================================

    print()
    print("=" * 60)
    print("RESUME SCORE")
    print("=" * 60)

    print(
        "Overall:",
        resume_data["overall_score"]
    )

    print(
        "Category:",
        resume_data["category"]
    )

    print(
        "ATS:",
        resume_data["ats_readability"]
    )

    print(
        "Experience:",
        resume_data["experience_fit"]
    )

    print(
        "Content:",
        resume_data["content_quality"]
    )

    print(
        "Job Match:",
        resume_data["job_match"]
    )

    print(
        "Skill Alignment:",
        resume_data["skill_alignment"]
    )

    print(
        "Formatting:",
        resume_data["formatting"]
    )

    print("=" * 60)

    # ========================================================
    # SAVE SMALL STRUCTURED DATA
    # ========================================================

    session["resume_analysis_data"] = resume_data

    # Keep the raw result for compatibility/debugging.
    # The structured result is what the new UI should use.
    session["resume_analysis"] = resume_data

    # ========================================================
    # SUCCESS
    # ========================================================

    flash(
        "Resume analyzed successfully!",
        "success"
    )

    # ========================================================
    # SHOW RESULT
    # ========================================================

    return render_resume_page(
        resume_data
    )