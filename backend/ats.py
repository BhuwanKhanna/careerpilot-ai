import re
from collections import Counter


# ============================================================
# ADVANCED ATS ANALYZER
# ============================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective",
        "about me"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "technologies",
        "technical competencies"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship experience",
        "internships"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
        "project experience"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "courses",
        "training"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
        "honors"
    ],

    "links": [
        "links",
        "profiles",
        "social profiles"
    ]
}


ACTION_VERBS = {
    "developed",
    "built",
    "created",
    "designed",
    "implemented",
    "engineered",
    "developed",
    "optimized",
    "improved",
    "automated",
    "analyzed",
    "tested",
    "deployed",
    "integrated",
    "managed",
    "led",
    "configured",
    "maintained",
    "debugged",
    "programmed",
    "architected",
    "launched",
    "delivered",
    "researched",
    "developed",
    "generated",
    "trained",
    "evaluated",
    "migrated",
    "streamlined",
    "coordinated",
    "executed",
    "resolved",
    "monitored",
    "documented"
}


TECHNICAL_KEYWORDS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "html",
    "css",
    "react",
    "react.js",
    "next.js",
    "node.js",
    "express",
    "fastapi",
    "django",
    "flask",
    "mongodb",
    "mysql",
    "postgresql",
    "firebase",
    "supabase",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "matlab",
    "linux",
    "rest api",
    "api",
    "excel",
    "power bi",
    "tableau",
    "figma",
    "tailwind",
    "bootstrap"
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = text.replace("\x00", " ")

    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# SECTION DETECTION
# ============================================================

def detect_sections(text):

    lower_text = text.lower()

    detected = {}

    for section, aliases in SECTION_ALIASES.items():

        found = False

        for alias in aliases:

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, lower_text):

                found = True
                break

        detected[section] = found

    return detected


# ============================================================
# CONTACT INFORMATION
# ============================================================

def analyze_contact_information(text):

    result = {
        "email": False,
        "phone": False,
        "linkedin": False,
        "github": False,
        "score": 0,
        "issues": []
    }

    # Email
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    if re.search(email_pattern, text):

        result["email"] = True
        result["score"] += 3

    else:

        result["issues"].append(
            "No valid email address detected."
        )


    # Phone
    phone_pattern = (
        r"(?:\+91[\s-]?)?"
        r"(?:\d[\s-]?){10,12}"
    )

    if re.search(phone_pattern, text):

        result["phone"] = True
        result["score"] += 3

    else:

        result["issues"].append(
            "No phone number detected."
        )


    # LinkedIn
    if "linkedin.com" in text.lower():

        result["linkedin"] = True
        result["score"] += 2

    else:

        result["issues"].append(
            "LinkedIn profile URL not detected."
        )


    # GitHub
    if "github.com" in text.lower():

        result["github"] = True
        result["score"] += 2

    else:

        result["issues"].append(
            "GitHub profile URL not detected."
        )


    return result


# ============================================================
# QUANTIFIED ACHIEVEMENTS
# ============================================================

def analyze_quantification(text):

    words = text.split()

    if not words:

        return {
            "count": 0,
            "score": 0,
            "issues": [
                "Resume contains no measurable achievements."
            ]
        }


    patterns = [

        r"\b\d+%\b",

        r"\b\d+\+",

        r"\b\d+x\b",

        r"\b\d+\s*(users|customers|clients|projects|people|students|records|employees)\b",

        r"\b\d+\s*(days|weeks|months|years)\b",

        r"\b₹\s*\d+",

        r"\$\s*\d+",

        r"\b\d+\s*(ms|seconds|minutes|hours)\b",

        r"\b\d+\.\d+\b"

    ]


    matches = []

    for pattern in patterns:

        matches.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )


    count = len(matches)


    if count >= 8:

        score = 10

    elif count >= 5:

        score = 8

    elif count >= 3:

        score = 6

    elif count >= 1:

        score = 3

    else:

        score = 0


    issues = []

    if count == 0:

        issues.append(
            "No quantified achievements detected. "
            "Add measurable results such as percentages, "
            "numbers, scale, time saved, users, or performance."
        )

    elif count < 3:

        issues.append(
            "Resume contains few quantified achievements."
        )


    return {
        "count": count,
        "score": score,
        "issues": issues
    }


# ============================================================
# ACTION VERBS
# ============================================================

def analyze_action_verbs(text):

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        text.lower()
    )

    found = set(words).intersection(
        ACTION_VERBS
    )

    count = len(found)


    if count >= 10:

        score = 8

    elif count >= 7:

        score = 7

    elif count >= 5:

        score = 5

    elif count >= 3:

        score = 3

    else:

        score = 1


    issues = []

    if count < 5:

        issues.append(
            "Use stronger action verbs such as "
            "developed, implemented, optimized, automated, "
            "analyzed, designed, or deployed."
        )


    return {
        "count": count,
        "verbs": sorted(found),
        "score": score,
        "issues": issues
    }


# ============================================================
# TECHNICAL SKILLS
# ============================================================

def analyze_technical_keywords(text):

    lower_text = text.lower()

    found = []

    for keyword in TECHNICAL_KEYWORDS:

        if keyword.lower() in lower_text:

            found.append(keyword)


    count = len(found)


    if count >= 15:

        score = 10

    elif count >= 10:

        score = 8

    elif count >= 7:

        score = 6

    elif count >= 4:

        score = 4

    elif count >= 1:

        score = 2

    else:

        score = 0


    issues = []

    if count == 0:

        issues.append(
            "No recognized technical keywords detected."
        )

    elif count < 5:

        issues.append(
            "Technical skill coverage appears limited."
        )


    return {
        "count": count,
        "keywords": sorted(found),
        "score": score,
        "issues": issues
    }


# ============================================================
# BULLET ANALYSIS
# ============================================================

def analyze_bullets(text):

    lines = text.splitlines()

    bullet_lines = []

    for line in lines:

        stripped = line.strip()

        if re.match(
            r"^[•●▪◦\-–—*]",
            stripped
        ):

            bullet_lines.append(
                stripped
            )


    if not bullet_lines:

        return {
            "count": 0,
            "quality": 0,
            "issues": [
                "No bullet points detected. "
                "Use concise bullet points for experience and projects."
            ]
        }


    strong_bullets = 0

    for bullet in bullet_lines:

        words = bullet.split()

        has_number = bool(
            re.search(
                r"\d",
                bullet
            )
        )

        first_word = (
            words[0]
            .strip("•●▪◦-*–—")
            .lower()
            if words
            else ""
        )

        if (
            first_word in ACTION_VERBS
            or has_number
        ):

            strong_bullets += 1


    percentage = (
        strong_bullets / len(bullet_lines)
    ) * 100


    if percentage >= 70:

        score = 8

    elif percentage >= 50:

        score = 6

    elif percentage >= 30:

        score = 4

    else:

        score = 2


    issues = []

    if percentage < 50:

        issues.append(
            "Several bullet points could be stronger "
            "by starting with action verbs and measurable results."
        )


    return {
        "count": len(bullet_lines),
        "strong": strong_bullets,
        "quality": score,
        "issues": issues
    }


# ============================================================
# LENGTH ANALYSIS
# ============================================================

def analyze_length(text):

    words = text.split()

    word_count = len(words)


    if word_count < 150:

        score = 3

        issue = (
            "Resume appears unusually short. "
            "Important information may be missing."
        )

    elif word_count <= 800:

        score = 8

        issue = None

    elif word_count <= 1100:

        score = 6

        issue = (
            "Resume is relatively long. "
            "Consider removing low-value content."
        )

    else:

        score = 3

        issue = (
            "Resume is very long and may contain unnecessary content."
        )


    issues = []

    if issue:

        issues.append(issue)


    return {
        "word_count": word_count,
        "score": score,
        "issues": issues
    }


# ============================================================
# DATE CONSISTENCY
# ============================================================

def analyze_dates(text):

    date_patterns = [

        r"\b20\d{2}\b",

        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*"
        r"\s+20\d{2}\b",

        r"\b\d{1,2}/\d{4}\b"

    ]


    dates = []

    for pattern in date_patterns:

        dates.extend(
            re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )
        )


    years = re.findall(
        r"\b20\d{2}\b",
        text
    )


    issues = []

    # Detect obviously unusual years
    for year in years:

        try:

            year_int = int(year)

            if year_int < 1990 or year_int > 2035:

                issues.append(
                    f"Unusual year detected: {year}."
                )

        except ValueError:

            pass


    score = 5 if dates else 2


    if not dates:

        issues.append(
            "No clear education or experience dates detected."
        )


    return {
        "count": len(dates),
        "score": score,
        "issues": issues
    }


# ============================================================
# REPETITION ANALYSIS
# ============================================================

def analyze_repetition(text):

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower()
    )


    stop_words = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "been",
        "were",
        "your",
        "their",
        "about",
        "using",
        "used",
        "into",
        "will",
        "which",
        "while",
        "where",
        "what",
        "when",
        "they",
        "them",
        "also"
    }


    meaningful_words = [
        word
        for word in words
        if word not in stop_words
    ]


    counter = Counter(
        meaningful_words
    )


    repeated = [
        (word, count)
        for word, count in counter.items()
        if count >= 8
    ]


    issues = []

    if len(repeated) >= 5:

        issues.append(
            "Several words appear repeatedly. "
            "Review the resume for unnecessary repetition."
        )


    return {
        "repeated_words": sorted(
            repeated,
            key=lambda x: x[1],
            reverse=True
        )[:10],
        "score": 5 if len(repeated) < 5 else 3,
        "issues": issues
    }


# ============================================================
# SECTION ANALYSIS
# ============================================================

def analyze_sections(text):

    sections = detect_sections(text)

    required_sections = [
        "education",
        "skills",
        "projects"
    ]

    recommended_sections = [
        "summary",
        "experience",
        "certifications",
        "achievements"
    ]


    score = 0
    issues = []


    # Required sections
    for section in required_sections:

        if sections[section]:

            score += 4

        else:

            issues.append(
                f"{section.title()} section not detected."
            )


    # Recommended sections
    for section in recommended_sections:

        if sections[section]:

            score += 2


    return {
        "sections": sections,
        "score": min(score, 20),
        "issues": issues
    }


# ============================================================
# PARSING / ATS COMPATIBILITY
# ============================================================

def analyze_parsing(text):

    issues = []

    score = 5


    if len(text.strip()) < 100:

        score = 0

        issues.append(
            "Very little text was extracted from the resume. "
            "The document may contain scanned images or "
            "complex formatting."
        )


    # Excessive special characters
    special_chars = len(
        re.findall(
            r"[^\w\s.,;:/@%()+\-#&]",
            text
        )
    )


    if special_chars > 100:

        score -= 2

        issues.append(
            "Large number of special characters detected. "
            "Review formatting for ATS compatibility."
        )


    # Very long lines can indicate columns/tables
    long_lines = sum(
        1
        for line in text.splitlines()
        if len(line) > 180
    )


    if long_lines > 5:

        score -= 2

        issues.append(
            "Complex text layout may affect parsing. "
            "Consider using a simple single-column structure."
        )


    score = max(
        0,
        min(score, 5)
    )


    return {
        "score": score,
        "issues": issues
    }


# ============================================================
# MAIN ATS FUNCTION
# ============================================================

def calculate_ats_score(resume):

    raw_text = resume.get(
        "raw_text",
        ""
    )


    text = normalize_text(
        raw_text
    )


    if not text:

        return {
            "score": 0,
            "grade": "F",
            "issues": [
                "No readable resume text was detected."
            ],
            "breakdown": {},
            "detected": {}
        }


    # Run analyses
    contact = analyze_contact_information(text)

    sections = analyze_sections(text)

    quantification = analyze_quantification(text)

    action_verbs = analyze_action_verbs(text)

    technical = analyze_technical_keywords(text)

    bullets = analyze_bullets(text)

    length = analyze_length(text)

    dates = analyze_dates(text)

    repetition = analyze_repetition(text)

    parsing = analyze_parsing(text)


    # ========================================================
    # WEIGHTED SCORE
    # ========================================================

    score = 0


    # Contact = 10
    score += contact["score"]


    # Sections = 20
    score += sections["score"]


    # Quantification = 10
    score += quantification["score"]


    # Action verbs = 8
    score += action_verbs["score"]


    # Technical keywords = 10
    score += technical["score"]


    # Bullet quality = 8
    score += bullets["quality"]


    # Length = 8
    score += length["score"]


    # Dates = 5
    score += dates["score"]


    # Repetition = 5
    score += repetition["score"]


    # Parsing = 5
    score += parsing["score"]


    # ========================================================
    # NORMALIZE TO 100
    # ========================================================

    maximum_possible = (
        10 +
        20 +
        10 +
        8 +
        10 +
        8 +
        8 +
        5 +
        5 +
        5
    )


    score = round(
        (score / maximum_possible) * 100
    )


    score = max(
        0,
        min(score, 100)
    )


    # ========================================================
    # GRADE
    # ========================================================

    if score >= 90:

        grade = "Excellent"

    elif score >= 80:

        grade = "Strong"

    elif score >= 70:

        grade = "Good"

    elif score >= 60:

        grade = "Needs Improvement"

    elif score >= 50:

        grade = "Weak"

    else:

        grade = "Poor"


    # ========================================================
    # COLLECT ISSUES
    # ========================================================

    all_issues = []


    analyses = [
        contact,
        sections,
        quantification,
        action_verbs,
        technical,
        bullets,
        length,
        dates,
        repetition,
        parsing
    ]


    for analysis in analyses:

        all_issues.extend(
            analysis.get(
                "issues",
                []
            )
        )


    # Remove duplicates
    unique_issues = []

    for issue in all_issues:

        if issue not in unique_issues:

            unique_issues.append(issue)


    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "score": score,

        "grade": grade,

        "issues": unique_issues,

        "breakdown": {

            "contact_information": contact["score"],

            "resume_sections": sections["score"],

            "quantified_achievements":
                quantification["score"],

            "action_verbs":
                action_verbs["score"],

            "technical_keywords":
                technical["score"],

            "bullet_quality":
                bullets["quality"],

            "resume_length":
                length["score"],

            "date_consistency":
                dates["score"],

            "repetition":
                repetition["score"],

            "ats_parsing":
                parsing["score"]

        },

        "detected": {

            "sections":
                sections["sections"],

            "technical_keywords":
                technical["keywords"],

            "action_verbs":
                action_verbs["verbs"],

            "quantified_achievements":
                quantification["count"],

            "bullet_points":
                bullets["count"],

            "strong_bullets":
                bullets["strong"],

            "word_count":
                length["word_count"],

            "contact": {

                "email":
                    contact["email"],

                "phone":
                    contact["phone"],

                "linkedin":
                    contact["linkedin"],

                "github":
                    contact["github"]

            }

        }

    }