from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

from parser import parse_resume
from ats import calculate_ats_score


app = FastAPI(
    title="AI Career Accelerator"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Upload folder
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Career Accelerator API is running"
    }


# --------------------------------------------------
# LinkedIn Summary Generator
# --------------------------------------------------

def generate_linkedin_summary(resume):

    name = resume.get(
        "name",
        "a motivated student"
    )

    text = resume.get(
        "raw_text",
        ""
    )

    text_lower = text.lower()


    # Detect common skills
    possible_skills = [
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "react",
        "html",
        "css",
        "sql",
        "machine learning",
        "data science",
        "fastapi",
        "git",
        "github",
        "matlab",
        "mongodb"
    ]


    found_skills = []

    for skill in possible_skills:

        if skill.lower() in text_lower:

            found_skills.append(skill)


    if found_skills:

        skills_text = ", ".join(
            found_skills[:8]
        )

    else:

        skills_text = "technology and problem solving"


    summary = f"""
I am {name}, a motivated student interested in
technology, problem solving and continuous learning.

I have developed skills in {skills_text} and enjoy
working on practical projects that help me understand
and apply what I learn.

I am currently focused on building my technical skills,
working on meaningful projects and gaining practical
experience through internships, projects and
collaboration.

I am always interested in learning new technologies,
solving challenging problems and connecting with people
who are working on interesting ideas.
""".strip()


    return summary


# --------------------------------------------------
# Resume Upload + Analysis
# --------------------------------------------------

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    allowed_extensions = [
        ".pdf",
        ".docx"
    ]


    extension = os.path.splitext(
        file.filename
    )[1].lower()


    # Check file type
    if extension not in allowed_extensions:

        return {
            "success": False,
            "message": "Only PDF and DOCX files are supported."
        }


    # Save file
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # --------------------------------------------------
    # STEP 7
    # Extract resume
    # --------------------------------------------------

    resume = parse_resume(
        file_path
    )


    # --------------------------------------------------
    # STEP 8
    # ATS analysis
    # --------------------------------------------------

    ats_result = calculate_ats_score(
        resume
    )


    # --------------------------------------------------
    # STEP 9
    # LinkedIn About
    # --------------------------------------------------

    linkedin_summary = generate_linkedin_summary(
        resume
    )


    # --------------------------------------------------
    # Final response
    # --------------------------------------------------

    return {

        "success": True,

        "message": "Resume analyzed successfully",

        "resume": resume,

        "ats": ats_result,

        "linkedin_summary": linkedin_summary
    }