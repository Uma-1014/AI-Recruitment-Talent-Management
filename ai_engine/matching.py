import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def normalize_text(text):
    """
    Clean and normalize text for AI matching.
    """
    if not text:
        return ""

    text = str(text).lower()

    # Keep letters, numbers, +, # and .
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    """
    Extract individual skills from comma-separated text.

    Example:
    'Python, Django, Machine Learning, SQL'
    ->
    {'python', 'django', 'machine learning', 'sql'}
    """

    if not text:
        return set()

    text = str(text).lower()

    skills = set()

    # First split by commas
    parts = text.split(",")

    for part in parts:
        skill = normalize_text(part)

        if skill:
            skills.add(skill)

    return skills


def calculate_skill_overlap(candidate_skills, required_skills):
    """
    Calculate explicit skill overlap percentage.

    This checks how many required skills are present
    in the candidate's skill set.
    """

    candidate_skill_set = extract_skills(candidate_skills)
    required_skill_set = extract_skills(required_skills)

    if not required_skill_set:
        return 0.0

    matched_skills = (
        candidate_skill_set.intersection(required_skill_set)
    )

    score = (
        len(matched_skills) /
        len(required_skill_set)
    ) * 100

    return round(min(score, 100.0), 2)


def calculate_tfidf_similarity(candidate_skills, required_skills):
    """
    Calculate TF-IDF cosine similarity between
    candidate skills and job-required skills.

    This provides lexical similarity beyond
    exact comma-separated skill matching.
    """

    candidate_text = normalize_text(candidate_skills)
    required_text = normalize_text(required_skills)

    if not candidate_text or not required_text:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        vectors = vectorizer.fit_transform(
            [
                candidate_text,
                required_text
            ]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(
            float(similarity * 100),
            2
        )

    except ValueError:
        return 0.0


def calculate_skills_score(
    candidate_skills,
    required_skills
):
    """
    Calculate the final skills score.

    We combine:
    - 70% explicit skill overlap
    - 30% TF-IDF similarity

    This makes the recruitment score more
    interpretable while still using NLP.
    """

    overlap_score = calculate_skill_overlap(
        candidate_skills,
        required_skills
    )

    tfidf_score = calculate_tfidf_similarity(
        candidate_skills,
        required_skills
    )

    final_score = (
        (overlap_score * 0.70) +
        (tfidf_score * 0.30)
    )

    return round(
        min(final_score, 100.0),
        2
    )


def calculate_experience_score(
    candidate_experience,
    required_experience
):
    """
    Calculate experience match percentage.
    """

    candidate_experience = float(
        candidate_experience or 0
    )

    required_experience = float(
        required_experience or 0
    )

    # If the job has no experience requirement,
    # the candidate receives full experience score.
    if required_experience <= 0:
        return 100.0

    score = (
        candidate_experience /
        required_experience
    ) * 100

    return round(
        min(score, 100.0),
        2
    )


def calculate_education_score(
    candidate_education,
    required_education
):
    """
    Calculate education similarity using
    keyword overlap.
    """

    candidate_text = normalize_text(
        candidate_education
    )

    required_text = normalize_text(
        required_education
    )

    if not candidate_text or not required_text:
        return 0.0

    candidate_words = set(
        candidate_text.split()
    )

    required_words = set(
        required_text.split()
    )

    if not required_words:
        return 0.0

    matching_words = (
        candidate_words.intersection(
            required_words
        )
    )

    score = (
        len(matching_words) /
        len(required_words)
    ) * 100

    return round(
        min(score, 100.0),
        2
    )


def generate_recommendation(overall_score):
    """
    Convert the numerical AI score into
    a recruitment recommendation.
    """

    if overall_score >= 80:
        return "Strong Match"

    elif overall_score >= 60:
        return "Good Match"

    elif overall_score >= 40:
        return "Potential Match"

    else:
        return "Low Match"


def calculate_match_score(candidate, job):
    """
    Calculate the complete AI candidate-job
    matching score.

    Weighting:
    - Skills: 60%
    - Experience: 25%
    - Education: 15%
    """

    skills_score = calculate_skills_score(
        candidate.skills,
        job.required_skills
    )

    experience_score = calculate_experience_score(
        candidate.experience_years,
        job.experience_required
    )

    education_score = calculate_education_score(
        candidate.education,
        job.education_required
    )

    # Overall weighted score
    overall_score = (
        (skills_score * 0.60) +
        (experience_score * 0.25) +
        (education_score * 0.15)
    )

    overall_score = round(
        min(overall_score, 100.0),
        2
    )

    recommendation = generate_recommendation(
        overall_score
    )

    return {
        "match_score": overall_score,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "recommendation": recommendation,
    }