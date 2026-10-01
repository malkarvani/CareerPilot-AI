# ==========================================================
# CAREERAI
# GROQ AI SERVICE
# ==========================================================
#
# This file contains the AI functions used by CareerAI.
#
# Main modules:
#
# 1. AI Chat
# 2. Resume Analyzer
# 3. Career Roadmap
# 4. Skill Gap Analyzer
# 5. Job Description Analyzer
# 6. Career Recommendation
# 7. Interview Preparation
# 8. Mock Interview Feedback
# 9. Course Recommendation
# 10. Certification Recommendation
# 11. Job Matching
# 12. Resume Summary
# 13. Cover Letter
# 14. Resume Rewriter
# 15. Skill Explainer
# 16. Project Generator
# 17. Study Planner
# 18. Learning Roadmap
# 19. Salary Estimator
# 20. Internship Advisor
# 21. Freelancing Advisor
# 22. SOP Generator
# 23. HR Answer Generator
# 24. Higher Studies Guide
# 25. Personal Career Mentor
# 26. Career Analytics
# 27. Weekly Learning Plan
# 28. Coding Practice Planner
# 29. AI Job Finder
# 30. AI Health Check
#
# ==========================================================


import os
import json
import re
import time
import logging


from dotenv import load_dotenv
from groq import Groq


# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("CareerAI")


# ==========================================================
# GROQ CONFIGURATION
# ==========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Current Groq model
MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are CareerAI, an expert AI career mentor.

You act as:

- Senior Career Mentor
- Resume Expert
- ATS Expert
- Technical Mentor
- HR Interviewer
- Career Counselor
- Job Preparation Mentor
- Learning Planner

Rules:

1. Give accurate and useful information.
2. Use simple English.
3. Be practical.
4. Personalize answers when user information is provided.
5. Use headings when appropriate.
6. Use bullet points when appropriate.
7. Do not give fake certifications.
8. Do not invent experience or achievements.
9. Keep resume advice ATS-friendly.
10. Consider the user's current skill level.
11. Give realistic career advice.
12. Focus on India unless another country is specified.
13. Avoid unnecessary repetition.
14. Give actionable next steps.
"""


# ==========================================================
# GROQ CLIENT
# ==========================================================

def get_groq_client():
    """
    Create a Groq client.

    The client is created when a function is called so that
    importing this file does not immediately crash when the
    API key is missing.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Please add GROQ_API_KEY=your_key to your .env file."
        )

    return Groq(
        api_key=api_key
    )


# ==========================================================
# COMMON AI FUNCTION
# ==========================================================

def ask_ai(
    prompt,
    temperature=0.3,
    max_tokens=5000,
    retries=3
):
    """
    Main function used by all CareerAI modules.

    Sends a prompt to Groq and returns the AI response.
    """

    client = get_groq_client()

    last_error = None


    for attempt in range(1, retries + 1):

        try:

            logger.info(
                "CareerAI AI request - attempt %s/%s",
                attempt,
                retries
            )


            response = client.chat.completions.create(

                model=MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=temperature,

                max_tokens=max_tokens
            )


            answer = (
                response
                .choices[0]
                .message
                .content
            )


            if not answer:

                raise RuntimeError(
                    "AI returned an empty response."
                )


            logger.info(
                "CareerAI AI response generated successfully."
            )


            return answer.strip()


        except Exception as error:

            last_error = error

            logger.warning(
                "AI attempt %s failed: %s",
                attempt,
                error
            )


            if attempt < retries:

                time.sleep(2)


    raise RuntimeError(
        f"Groq AI request failed: {last_error}"
    )


# ==========================================================
# COMPATIBILITY ALIAS
# ==========================================================

def generate_ai_response(
    prompt,
    system_message=None,
    temperature=0.3,
    max_tokens=5000
):
    """
    Compatibility function used by newer routes/services.
    """

    if system_message:

        client = get_groq_client()


        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=temperature,

            max_tokens=max_tokens
        )


        answer = (
            response
            .choices[0]
            .message
            .content
        )


        return answer.strip()


    return ask_ai(
        prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )


# Old project compatibility
generate_response = ask_ai


# ==========================================================
# PROMPT BUILDER
# ==========================================================

def create_prompt(title, content):
    """
    Creates a standard CareerAI prompt.
    """

    return f"""
# {title}

{content}

Requirements:

- Professional
- Practical
- Clear
- Easy to understand
- Use headings
- Use bullet points
- Give actionable advice
"""


# ==========================================================
# ==========================================================
# CAREER CHAT
# ==========================================================
# ==========================================================

def career_chat(user_message):

    prompt = f"""
You are CareerAI's personal career advisor.

Answer the student's question professionally.

Student Question:

{user_message}

Give:

1. Direct answer
2. Explanation
3. Practical advice
4. Recommended next steps

Keep the answer useful and easy to understand.
"""

    return ask_ai(
        prompt,
        temperature=0.5,
        max_tokens=3000
    )


# ==========================================================
# ==========================================================
# RESUME ANALYZER
# ==========================================================
# ==========================================================

def _clean_json_response(text):

    if not text:

        raise ValueError(
            "AI returned an empty response."
        )


    text = text.strip()


    # Remove markdown JSON blocks

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )


    text = re.sub(
        r"\s*```$",
        "",
        text
    ).strip()


    # Find JSON object

    first = text.find("{")

    last = text.rfind("}")


    if first != -1 and last != -1:

        text = text[
            first:last + 1
        ]


    return text


def _safe_score(value, default=0):

    try:

        value = int(
            float(value)
        )

    except (
        TypeError,
        ValueError
    ):

        value = default


    return max(
        0,
        min(
            100,
            value
        )
    )


def _safe_list(value):

    if value is None:

        return []


    if isinstance(value, list):

        result = []


        for item in value:

            if isinstance(item, str):

                item = item.strip()

                if item:

                    result.append(item)


            elif isinstance(item, dict):

                if "text" in item:

                    text = str(
                        item["text"]
                    ).strip()

                    if text:

                        result.append(text)


        return result


    if isinstance(value, str):

        result = []


        for line in value.splitlines():

            line = line.strip()


            line = re.sub(
                r"^[-•*]\s*",
                "",
                line
            )


            line = re.sub(
                r"^\d+[\.\)]\s*",
                "",
                line
            )


            if line:

                result.append(line)


        return result


    return []


def _normalize_career_suggestions(value):

    if not isinstance(value, list):

        return []


    result = []


    for item in value:

        if isinstance(item, dict):

            career = str(
                item.get(
                    "career",
                    ""
                )
            ).strip()


            reason = str(
                item.get(
                    "reason",
                    ""
                )
            ).strip()


            if career:

                result.append(
                    {
                        "career": career,
                        "reason": reason
                    }
                )


        elif isinstance(item, str):

            item = item.strip()


            if item:

                result.append(
                    {
                        "career": item,
                        "reason": ""
                    }
                )


    return result


def get_resume_category(score):

    score = _safe_score(score)


    if score < 40:

        return "Poor"


    if score < 75:

        return "Average"


    if score <= 90:

        return "Good"


    return "Excellent"


def analyze_resume(resume_text):

    if not resume_text or not resume_text.strip():

        raise ValueError(
            "Resume text is empty."
        )


    resume_text = resume_text.strip()


    if len(resume_text) > 50000:

        resume_text = resume_text[
            :50000
        ]


    prompt = f"""
You are CareerAI's professional ATS resume analysis engine.

Analyze the resume carefully.

Return ONLY valid JSON.

Do not return:
- Markdown
- ```json
- tables
- explanations outside JSON

Use EXACTLY this structure:

{{
    "overall_score": 0,
    "ats_readability": 0,
    "experience_fit": 0,
    "content_quality": 0,
    "job_match": 0,
    "skill_alignment": 0,
    "formatting": 0,

    "strengths": [
        "strength 1",
        "strength 2",
        "strength 3",
        "strength 4"
    ],

    "improvements": [
        "improvement 1",
        "improvement 2",
        "improvement 3",
        "improvement 4"
    ],

    "skills": [
        "Python",
        "SQL",
        "Git"
    ],

    "ats_improvements": [
        "ATS improvement 1",
        "ATS improvement 2",
        "ATS improvement 3",
        "ATS improvement 4"
    ],

    "career_suggestions": [
        {{
            "career": "Career title",
            "reason": "Why this career matches the resume"
        }},
        {{
            "career": "Career title",
            "reason": "Why this career matches the resume"
        }},
        {{
            "career": "Career title",
            "reason": "Why this career matches the resume"
        }}
    ],

    "summary": "Short professional summary."
}}


SCORING RULES:

Overall score should be realistic.

Consider:

- ATS readability
- Resume structure
- Skills
- Projects
- Experience
- Achievements
- Keywords
- Formatting
- Career alignment
- Content quality

Do not automatically give a high score.

A beginner resume can receive a lower score.

Give useful recommendations.

Resume:

{resume_text}
"""


    raw_response = ask_ai(

        prompt,

        temperature=0.2,

        max_tokens=5000
    )


    try:

        cleaned = _clean_json_response(
            raw_response
        )


        data = json.loads(
            cleaned
        )


    except Exception as error:

        logger.error(
            "Resume JSON parsing error: %s",
            error
        )

        logger.error(
            "AI response: %s",
            raw_response
        )


        raise ValueError(
            "AI returned an invalid resume analysis format."
        )


    # ------------------------------------------------------
    # NORMALIZE SCORES
    # ------------------------------------------------------

    score_fields = [

        "overall_score",

        "ats_readability",

        "experience_fit",

        "content_quality",

        "job_match",

        "skill_alignment",

        "formatting"

    ]


    for field in score_fields:

        data[field] = _safe_score(
            data.get(field)
        )


    # ------------------------------------------------------
    # CATEGORY
    # ------------------------------------------------------

    data["category"] = get_resume_category(
        data["overall_score"]
    )


    # ------------------------------------------------------
    # LISTS
    # ------------------------------------------------------

    data["strengths"] = _safe_list(
        data.get("strengths")
    )


    data["improvements"] = _safe_list(
        data.get("improvements")
    )


    data["skills"] = _safe_list(
        data.get("skills")
    )


    data["ats_improvements"] = _safe_list(
        data.get("ats_improvements")
    )


    data["career_suggestions"] = (
        _normalize_career_suggestions(
            data.get(
                "career_suggestions"
            )
        )
    )


    # ------------------------------------------------------
    # DEFAULT VALUES
    # ------------------------------------------------------

    if not data["strengths"]:

        data["strengths"] = [
            "Resume contains relevant career information."
        ]


    if not data["improvements"]:

        data["improvements"] = [
            "Add more measurable achievements."
        ]


    if not data["ats_improvements"]:

        data["ats_improvements"] = [
            "Improve role-specific keyword coverage."
        ]


    if not data["career_suggestions"]:

        data["career_suggestions"] = [
            {
                "career": "Software Developer",
                "reason": "Your technical skills may align with software development roles."
            }
        ]


    data["summary"] = str(
        data.get(
            "summary",
            ""
        )
    ).strip()


    if not data["summary"]:

        data["summary"] = (
            "CareerAI analyzed your resume and "
            "identified opportunities to improve "
            "ATS readiness, skills presentation, "
            "career alignment and overall impact."
        )


    return data


# ==========================================================
# OLD RESUME SCORE FUNCTION
# ==========================================================

def calculate_resume_score(resume_text):

    prompt = f"""
Analyze this resume.

Resume:

{resume_text}

Return:

1. Overall Score /100
2. ATS Score /100
3. Technical Skills Score
4. Formatting Score
5. Grammar Score
6. Experience Score
7. Top Improvements
"""

    return ask_ai(
        prompt,
        temperature=0.3
    )


# ==========================================================
# ==========================================================
# CAREER ROADMAP
# ==========================================================
# ==========================================================

def generate_career_roadmap(
    career_goal,
    current_level="Beginner",
    education="Not specified",
    experience="Not specified",
    skills="Not specified",
    additional_info="Not specified"
):
    """
    Generate a clear, personalized CareerAI roadmap.

    The prompt intentionally avoids Markdown tables because the frontend
    roadmap renderer is designed for simple headings and bullet points.
    """

    career_goal = str(career_goal or "").strip() or "Not specified"
    current_level = str(current_level or "Beginner").strip() or "Beginner"
    education = str(education or "Not specified").strip() or "Not specified"
    experience = str(experience or "Not specified").strip() or "Not specified"
    skills = str(skills or "Not specified").strip() or "Not specified"
    additional_info = (
        str(additional_info or "Not specified").strip()
        or "Not specified"
    )

    prompt = f"""
You are CareerAI's expert career roadmap generator.

Create a personalized, practical and easy-to-follow career roadmap for the
student below. The roadmap must take the student from their CURRENT LEVEL
towards job readiness for the TARGET CAREER.

STUDENT INFORMATION
-------------------
Target Career: {career_goal}
Current Level: {current_level}
Education: {education}
Experience: {experience}
Current Skills: {skills}
Additional Information: {additional_info}

PERSONALIZATION RULES
---------------------
1. Start from the student's current level.
2. Do not give advanced topics before the required foundations.
3. Avoid repeating skills the student already knows unless they need deeper
   knowledge for the target role.
4. Connect every learning stage to practical work and employability.
5. Keep the order logical: foundation -> core skills -> projects -> advanced
   skills -> portfolio -> certifications -> interview -> job preparation.
6. Use simple English. A beginner should be able to understand what to do.
7. Give concrete technologies, tools, practice tasks and project ideas when
   they are relevant to the target career.
8. Do not invent facts about the student.
9. Do not claim a certification is mandatory unless it genuinely is.
10. If a section is not relevant to the target career, explain that briefly
    instead of adding unrelated content.

VERY IMPORTANT FORMATTING RULES
-------------------------------
- Return ONLY the roadmap in Markdown.
- DO NOT use Markdown tables.
- DO NOT use the pipe character | for tables or table separators.
- DO NOT create rows such as | Topic | Tool | Project |.
- DO NOT use table separator lines such as |---|---|.
- Use normal headings and bullet points only.
- Use exactly the step headings shown below.
- Each step must have the requested subsections.
- Keep each bullet short and direct.
- Explain what the student should actually do, not only what a topic means.
- Do not add a section called "What should you do today".

REQUIRED ROADMAP STRUCTURE
==========================

# Career Goal

Briefly explain:
- What the target role does
- Where these skills are commonly used
- What the student should be able to do by the end of the roadmap

# STEP 1 — Foundation

### What You Will Learn
- List the foundation topics in the correct order.

### Important Concepts
- Explain the concepts the student must understand.

### Tools and Technologies
- List the tools or technologies to learn.

### Practice
- Give practical exercises.

### Small Project
- Give one small project that applies the foundation.

### Expected Result
- Explain what the student should be able to do after this step.

# STEP 2 — Core Skills

### Technical Skills
- List the core technical skills in learning order.

### Tools and Frameworks
- List relevant tools, libraries, frameworks or platforms.

### Practice Tasks
- Give practical tasks that build confidence.

### Project
- Give one useful project for this stage.

### Expected Result
- Explain the capability gained.

# STEP 3 — Projects

### Beginner Project
- Give one realistic beginner project.

### Intermediate Project
- Give one realistic intermediate project.

### Advanced Project
- Give one realistic advanced project.

### What to Build
- Explain the important features to implement.

### Technologies
- List the recommended stack.

### Resume Value
- Explain what each project demonstrates to employers.

# STEP 4 — Advanced Skills

### Advanced Topics
- List advanced skills needed for the target career.

### Real-World Skills
- Explain production, teamwork, debugging, security, scalability or other
  real-world skills relevant to the role.

### Practice
- Give advanced practice tasks.

### Expected Result
- Explain what the student should be capable of at the end.

# STEP 5 — Portfolio

### GitHub
- Explain what repositories to create and how to organize them.

### README Files
- Explain what each project README should contain.

### Portfolio Website
- Explain the sections the website should include.

### Project Presentation
- Explain how to demonstrate projects clearly.

### Resume Evidence
- Explain which projects and achievements should be highlighted.

# STEP 6 — Certifications

### Recommended Certifications
- List only relevant, legitimate certifications.
- Explain why each can be useful.
- Mention when a certification is optional.

### Alternative Proof of Skill
- Explain practical alternatives such as projects, GitHub work, internships
  or recognized assessments when appropriate.

# STEP 7 — Interview Preparation

### HR Preparation
- List important HR topics and questions to practice.

### Technical Preparation
- List the technical topics to revise.

### Coding Preparation
- Give coding/problem-solving areas when relevant.

### Project Questions
- List questions the student should be ready to answer about their projects.

### Behavioral Questions
- Give practical behavioral preparation.

### Mock Interviews
- Give a simple mock interview practice method.

# STEP 8 — Job Preparation

### Resume
- Give specific resume preparation actions.

### LinkedIn
- Give specific LinkedIn profile actions.

### Job Applications
- Explain how to search, target and apply for relevant roles.

### Networking
- Give practical networking actions.

### Internships and Entry Roles
- Explain suitable entry points for the student's current level.

### Application Tracking
- Give a simple way to track applications and follow-ups.

# STEP 9 — 90 DAY PLAN

### Days 1-30
- Give specific learning, practice and project actions.

### Days 31-60
- Give specific project, portfolio and skill-building actions.

### Days 61-90
- Give specific interview, application and job-readiness actions.

### 90-Day Outcome
- Explain what the student should have completed by day 90.

# Final Career Journey

### What Success Looks Like
- Give a short, realistic description of the student's next stage.

### Final Mentor Message
- Give a short motivating message focused on consistent action.

FINAL QUALITY CHECK
===================
Before responding, verify that:
- Steps are numbered exactly 1 through 9.
- The roadmap is personalized to the supplied student information.
- The sequence is logical.
- No Markdown tables or pipe-separated rows appear anywhere.
- The language is simple and direct.
- Every step contains useful actions.
- No fake student experience or achievements are added.
- No "What should you do today" section is included.
"""

    return ask_ai(
        prompt,
        temperature=0.3,
        max_tokens=6500
    )


# ==========================================================
# SIMPLE ROADMAP COMPATIBILITY FUNCTION
# ==========================================================

def generate_roadmap(career_goal):

    return generate_career_roadmap(
        career_goal=career_goal
    )


# ==========================================================
# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================
# ==========================================================

def analyze_skill_gap(
    current_skills,
    target_role
):

    prompt = f"""
Analyze the skill gap.

Target Role:

{target_role}

Current Skills:

{current_skills}

Provide:

1. Matching Skills
2. Missing Skills
3. Priority Learning Order
4. Recommended Courses
5. Recommended Projects
6. Estimated Learning Time
7. Final Readiness Percentage
8. Next Steps

Use clear headings and bullet points.
"""

    return ask_ai(prompt)


# Compatibility alias

def skill_gap(
    skills,
    career
):

    return analyze_skill_gap(
        current_skills=skills,
        target_role=career
    )


# ==========================================================
# ==========================================================
# JOB DESCRIPTION ANALYSIS
# ==========================================================
# ==========================================================

def analyze_job_description(
    job_description
):

    prompt = f"""
Analyze this job description.

JOB DESCRIPTION:

{job_description}

Provide:

1. Required Technical Skills
2. Soft Skills
3. Experience Level
4. Important Keywords
5. Responsibilities
6. ATS Keywords
7. Resume Optimization Tips
8. Interview Topics
9. Missing Skills
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# CAREER RECOMMENDATION
# ==========================================================
# ==========================================================

def recommend_career(
    skills,
    interests
):

    prompt = f"""
Recommend suitable careers.

Skills:

{skills}

Interests:

{interests}

Provide:

1. Best Career Options
2. Why Each Career Fits
3. Required Skills
4. Certifications
5. Growth Opportunities
6. Future Scope
7. Suggested First Job
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# INTERVIEW QUESTION GENERATOR
# ==========================================================
# ==========================================================

def generate_interview_questions(
    job_role,
    experience="Fresher"
):

    prompt = f"""
Create an interview preparation guide.

Role:

{job_role}

Experience:

{experience}

Include:

1. HR Questions
2. Technical Questions
3. Coding Questions
4. Scenario Questions
5. Behavioral Questions
6. Questions about Projects
7. Tips to Answer
8. Common Mistakes
"""

    return ask_ai(
        prompt,
        temperature=0.5,
        max_tokens=5000
    )


# Compatibility name

def interview_questions(role):

    return generate_interview_questions(
        job_role=role
    )


# ==========================================================
# MOCK INTERVIEW FEEDBACK
# ==========================================================

def interview_feedback(
    question,
    answer
):

    prompt = f"""
Evaluate this interview answer.

QUESTION:

{question}

CANDIDATE ANSWER:

{answer}

Provide:

1. Score /10
2. Strengths
3. Weaknesses
4. Better Answer
5. Communication Tips
6. What the interviewer may think
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# COURSE RECOMMENDATION
# ==========================================================
# ==========================================================

def recommend_courses(skill):

    prompt = f"""
Recommend learning resources for:

{skill}

Include:

- Free courses
- Paid courses
- YouTube channels
- Official documentation
- Practice websites
- Projects
- Estimated learning duration
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# CERTIFICATION RECOMMENDATION
# ==========================================================
# ==========================================================

def recommend_certifications(career):

    prompt = f"""
Recommend useful industry-recognized certifications for:

{career}

For each certification provide:

- Certification name
- Provider
- Difficulty
- Cost
- Duration
- Skills covered
- Industry value
- Whether it is useful for beginners
"""

    return ask_ai(prompt)


# Compatibility alias

def recommend_certificates(career):

    return recommend_certifications(
        career
    )


# ==========================================================
# ==========================================================
# RESUME + JOB MATCH
# ==========================================================
# ==========================================================

def match_resume_job(
    resume_text,
    job_description
):

    prompt = f"""
Compare this resume with this job description.

RESUME:

{resume_text}

JOB DESCRIPTION:

{job_description}

Provide:

1. Match Percentage
2. Matching Skills
3. Missing Skills
4. Missing Keywords
5. Experience Match
6. Resume Improvements
7. ATS Optimization Tips
8. Final Recommendation
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# RESUME SUMMARY
# ==========================================================
# ==========================================================

def generate_resume_summary(
    skills,
    experience,
    goal
):

    prompt = f"""
Create professional ATS-friendly resume summaries.

Skills:

{skills}

Experience:

{experience}

Career Goal:

{goal}

Create:

1. Professional Version
2. ATS Version
3. Fresher Version

Each should be approximately 80-120 words.
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# COVER LETTER
# ==========================================================
# ==========================================================

def generate_cover_letter(
    name,
    company,
    job_title,
    skills
):

    prompt = f"""
Write a professional personalized cover letter.

Applicant:

{name}

Company:

{company}

Position:

{job_title}

Skills:

{skills}

Requirements:

- Professional
- Personalized
- ATS-friendly
- Around 300-400 words
- Strong opening
- Strong closing
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# RESUME REWRITER
# ==========================================================
# ==========================================================

def rewrite_resume(resume_text):

    prompt = f"""
Rewrite the following resume professionally.

Resume:

{resume_text}

Requirements:

- ATS-friendly
- Professional language
- Strong action verbs
- Correct grammar
- Clear structure
- Quantifiable achievements where supported
- Do not invent facts
- Keep facts accurate
"""

    return ask_ai(
        prompt,
        temperature=0.3,
        max_tokens=6000
    )


# ==========================================================
# ==========================================================
# SKILL EXPLAINER
# ==========================================================
# ==========================================================

def explain_skill(skill):

    prompt = f"""
Explain the following technology or skill:

{skill}

Include:

1. What is it?
2. Why is it important?
3. Where is it used?
4. Beginner learning path
5. Intermediate learning path
6. Advanced learning path
7. Projects
8. Interview questions
9. Career value
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# PROJECT IDEA GENERATOR
# ==========================================================
# ==========================================================

def generate_project_ideas(
    skill,
    level
):

    prompt = f"""
Generate project ideas.

Technology:

{skill}

Difficulty:

{level}

For each project include:

- Title
- Description
- Features
- Tech Stack
- Difficulty
- Estimated Time
- Skills learned
- Resume value
- GitHub value
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# DAILY STUDY PLANNER
# ==========================================================
# ==========================================================

def create_study_plan(
    goal,
    available_hours
):

    prompt = f"""
Create a practical study plan.

Goal:

{goal}

Daily available time:

{available_hours} hours

Include:

- Daily tasks
- Weekly goals
- Monthly milestones
- Practice
- Revision
- Projects
- Assessment
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# LEARNING ROADMAP
# ==========================================================
# ==========================================================

def learning_roadmap(skill):

    prompt = f"""
Create a complete learning roadmap for:

{skill}

Include:

1. Beginner Topics
2. Intermediate Topics
3. Advanced Topics
4. Practice
5. Projects
6. Books
7. Documentation
8. YouTube Resources
9. Certifications
10. Interview Preparation
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# SALARY ESTIMATOR
# ==========================================================
# ==========================================================

def estimate_salary(
    role,
    experience,
    location="India"
):

    prompt = f"""
Estimate realistic salary information.

Role:

{role}

Experience:

{experience}

Location:

{location}

Provide:

- Entry-level salary
- Mid-level salary
- Senior salary
- Important skills affecting salary
- Career growth
- Factors that increase salary

Clearly state that salary varies by company,
location, skills and market conditions.
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# INTERNSHIP ADVISOR
# ==========================================================
# ==========================================================

def internship_advice(
    skills,
    interests
):

    prompt = f"""
Recommend internships.

Skills:

{skills}

Interests:

{interests}

Provide:

- Suitable internship roles
- Required skills
- Projects to build
- Recommended platforms
- Preparation tips
- Expected internship responsibilities
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# FREELANCING ADVISOR
# ==========================================================
# ==========================================================

def freelancing_advice(skills):

    prompt = f"""
Provide freelancing guidance.

Skills:

{skills}

Include:

- Suitable freelance services
- Freelance platforms
- Portfolio ideas
- Pricing strategy
- Client acquisition
- Proposal tips
- Beginner mistakes
- Growth strategy
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# SOP GENERATOR
# ==========================================================
# ==========================================================

def generate_sop(
    student_details,
    university,
    course
):

    prompt = f"""
Write a professional Statement of Purpose.

Student Details:

{student_details}

University:

{university}

Course:

{course}

Requirements:

- 700-1000 words
- Professional
- Natural
- Unique
- Academic
- Strong motivation
- Career goals
- Strong conclusion
"""

    return ask_ai(
        prompt,
        temperature=0.5,
        max_tokens=5000
    )


# ==========================================================
# ==========================================================
# HR ANSWER GENERATOR
# ==========================================================
# ==========================================================

def hr_answer(
    question,
    profile
):

    prompt = f"""
Create an excellent HR interview answer.

Question:

{question}

Candidate Profile:

{profile}

Requirements:

- Professional
- Natural
- Confident
- Personalized
- Use STAR method where appropriate
- Avoid fake information
- Around 2-3 minutes speaking length
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# HIGHER STUDIES GUIDE
# ==========================================================
# ==========================================================

def higher_studies_guidance(
    course,
    country
):

    prompt = f"""
Provide higher studies guidance.

Course:

{course}

Country:

{country}

Include:

- University types
- Eligibility
- Entrance exams
- English tests
- Scholarships
- Approximate cost categories
- Application process
- Career opportunities
- Important documents
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# PERSONAL CAREER MENTOR
# ==========================================================
# ==========================================================

def personal_career_mentor(profile):

    prompt = f"""
Act as a personal career mentor.

Student Profile:

{profile}

Provide:

1. Career Direction
2. Strengths
3. Weaknesses
4. Skills to Learn
5. 12-Month Learning Plan
6. Recommended Projects
7. Certifications
8. Job Preparation
9. Interview Preparation
10. Motivation
"""

    return ask_ai(
        prompt,
        temperature=0.5,
        max_tokens=5000
    )


# ==========================================================
# ==========================================================
# CAREER ANALYTICS
# ==========================================================
# ==========================================================

def career_analytics(profile):

    prompt = f"""
Analyze this career profile.

Profile:

{profile}

Provide:

1. Career Readiness Score
2. Technical Skills Analysis
3. Soft Skills Analysis
4. Market Demand
5. Missing Skills
6. Career Growth
7. Recommendations
8. Next 3 Actions
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# WEEKLY LEARNING PLAN
# ==========================================================
# ==========================================================

def weekly_learning_plan(
    goal,
    hours_per_day
):

    prompt = f"""
Create a weekly learning plan.

Goal:

{goal}

Available Hours Per Day:

{hours_per_day}

Create:

Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
Sunday

Include:

- Topics
- Practice
- Projects
- Revision
- Weekly assessment
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# CODING PRACTICE PLANNER
# ==========================================================
# ==========================================================

def coding_practice_plan(
    language,
    level
):

    prompt = f"""
Create a coding practice plan.

Programming Language:

{language}

Level:

{level}

Include:

- Fundamentals
- Easy problems
- Medium problems
- Advanced problems
- Data structures
- Algorithms
- Practice schedule
- Project
- Interview preparation
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# AI JOB FINDER
# ==========================================================
# ==========================================================

def ai_job_finder(
    role,
    location="India"
):

    prompt = f"""
Help the student prepare for job searching.

Preferred Role:

{role}

Preferred Location:

{location}

Provide:

1. Suitable job titles
2. Skills commonly required
3. Experience expectations
4. Resume keywords
5. Portfolio requirements
6. Companies or company types to research
7. Job-search strategy
8. Application strategy
9. Networking strategy
10. Career growth

Important:

Do not claim real-time job openings unless current
job data is explicitly provided.
"""

    return ask_ai(prompt)


# ==========================================================
# ==========================================================
# AI STATUS
# ==========================================================
# ==========================================================

def ai_status():

    try:

        response = ask_ai(
            "Reply only with OK.",
            temperature=0,
            max_tokens=20,
            retries=1
        )


        return bool(response)


    except Exception as error:

        logger.error(
            "AI health check failed: %s",
            error
        )


        return False


# ==========================================================
# ==========================================================
# VERSION
# ==========================================================
# ==========================================================

def version():

    return {

        "application": "CareerAI",

        "version": "3.0",

        "provider": "Groq",

        "model": MODEL

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("CareerAI Groq AI Service")

    print("=" * 60)

    print()

    print(
        "Model:",
        MODEL
    )

    print()

    if ai_status():

        print(
            "AI Status: CONNECTED"
        )

        print()

        print(
            generate_roadmap(
                "Python Full Stack Developer"
            )
        )

    else:

        print(
            "AI Status: NOT CONNECTED"
        )

        print(
            "Check GROQ_API_KEY in your .env file."
        )