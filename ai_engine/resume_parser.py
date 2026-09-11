import re
from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX resume.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_resume_text(file_path):
    """
    Detect the resume file type and extract text.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":

        return extract_text_from_pdf(file_path)

    elif extension == ".docx":

        return extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported resume format. "
            "Please upload a PDF or DOCX file."
        )


def clean_text(text):
    """
    Clean extracted resume text.
    """

    if not text:
        return ""

    text = text.replace("\x00", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_email(text):
    """
    Extract the first email address from resume text.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group(0)

    return ""


def extract_phone(text):
    """
    Extract a likely phone number.
    """

    pattern = (
        r"(?<!\d)"
        r"(?:\+91[\s-]?)?"
        r"(?:\d[\s-]?){10}"
        r"(?!\d)"
    )

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group(0).strip()

    return ""


def extract_skills(text):
    """
    Detect common technical skills from resume text.
    """

    skill_dictionary = [

        "python",
        "java",
        "c++",
        "c",
        "javascript",
        "typescript",

        "django",
        "flask",
        "fastapi",
        "react",
        "node.js",

        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",

        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",

        "sql",
        "mysql",
        "postgresql",
        "mongodb",

        "power bi",
        "tableau",
        "excel",

        "git",
        "github",
        "docker",
        "aws",

        "statistics",
        "nlp",
        "computer vision",
    ]

    text_lower = text.lower()

    detected_skills = []

    for skill in skill_dictionary:

        if skill.lower() in text_lower:

            detected_skills.append(skill)

    return detected_skills


def extract_experience_years(text):
    """
    Extract years of experience from resume text.
    """

    patterns = [

        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s*(?:of)?\s*experience",

        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*years?",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text.lower()
        )

        if match:

            try:

                return float(
                    match.group(1)
                )

            except ValueError:

                pass

    return 0.0


def extract_education(text):
    """
    Detect common education qualifications.
    """

    education_keywords = [

        "b.tech",
        "btech",
        "b.e",
        "be ",
        "bachelor",
        "b.sc",
        "bsc",

        "m.tech",
        "mtech",
        "m.e",
        "me ",
        "master",
        "m.sc",
        "msc",

        "mba",
        "phd",
        "ph.d",

    ]

    text_lower = text.lower()

    detected = []

    for keyword in education_keywords:

        if keyword in text_lower:

            detected.append(
                keyword.strip()
            )

    return list(
        dict.fromkeys(detected)
    )


def parse_resume(file_path):
    """
    Complete AI resume parsing pipeline.

    Returns structured candidate information.
    """

    raw_text = extract_resume_text(
        file_path
    )

    text = clean_text(
        raw_text
    )

    skills = extract_skills(
        text
    )

    experience_years = extract_experience_years(
        text
    )

    education = extract_education(
        text
    )

    email = extract_email(
        text
    )

    phone = extract_phone(
        text
    )

    return {

        "raw_text": text,

        "email": email,

        "phone": phone,

        "skills": skills,

        "experience_years": experience_years,

        "education": education,

    }