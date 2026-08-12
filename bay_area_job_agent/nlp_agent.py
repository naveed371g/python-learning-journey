import re
import string
import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

for resource in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.data.find(
            f"tokenizers/{resource}" if resource.startswith("punkt") else f"corpora/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

TECH_SKILLS = {
    "python", "java", "javascript", "typescript", "go", "golang", "rust", "c++", "c#", "ruby",
    "scala", "kotlin", "swift", "r", "matlab", "bash", "shell", "sql", "nosql",
    "react", "angular", "vue", "node", "nodejs", "django", "flask", "fastapi", "spring", "rails",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "keras", "huggingface",
    "aws", "azure", "gcp", "kubernetes", "k8s", "docker", "terraform", "ansible",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "kafka", "spark",
    "git", "ci/cd", "jenkins", "github", "gitlab", "linux", "unix",
    "machine learning", "deep learning", "nlp", "llm", "ai", "data science",
    "devops", "mlops", "sre", "microservices", "rest", "graphql", "api",
    "agile", "scrum", "jira", "figma",
}

JOB_TITLE_KEYWORDS = {
    "software engineer", "software developer", "swe", "backend engineer", "frontend engineer",
    "full stack", "fullstack", "full-stack", "data scientist", "data engineer", "data analyst",
    "ml engineer", "machine learning engineer", "ai engineer", "devops engineer",
    "site reliability engineer", "sre", "platform engineer", "cloud engineer",
    "mobile developer", "ios developer", "android developer", "product manager", "pm",
    "engineering manager", "tech lead", "staff engineer", "principal engineer",
    "qa engineer", "test engineer", "security engineer", "network engineer",
    "solutions architect", "cloud architect", "system administrator", "sysadmin",
    "data architect", "database administrator", "dba", "web developer",
    "ui developer", "ux engineer", "research engineer", "research scientist",
}

SENIORITY_MAP = {
    "junior": ["junior", "jr", "entry level", "entry-level", "new grad", "intern", "internship", "associate"],
    "mid": ["mid", "mid-level", "intermediate", "ii", "level 2"],
    "senior": ["senior", "sr", "lead", "principal", "staff", "iii", "iv", "v", "level 3", "level 4", "level 5"],
    "manager": ["manager", "director", "head of", "vp", "vice president", "cto", "engineering manager"],
}

JOB_TYPE_MAP = {
    "remote": ["remote", "work from home", "wfh", "fully remote", "distributed"],
    "hybrid": ["hybrid", "partial remote", "flexible"],
    "onsite": ["onsite", "on-site", "in office", "in-office", "on site"],
}

STOP_WORDS = set(stopwords.words("english"))


def extract_profile(user_text: str) -> dict:
    """Extract job search intent from free-form user text."""
    text_lower = user_text.lower()
    tokens = word_tokenize(text_lower)
    tokens = [t for t in tokens if t not in string.punctuation]

    skills = []
    for skill in TECH_SKILLS:
        if skill in text_lower:
            skills.append(skill)

    job_title = ""
    for title in sorted(JOB_TITLE_KEYWORDS, key=len, reverse=True):
        if title in text_lower:
            job_title = title
            break

    seniority = "any"
    for level, keywords in SENIORITY_MAP.items():
        if any(kw in text_lower for kw in keywords):
            seniority = level
            break

    job_type = "any"
    for jtype, keywords in JOB_TYPE_MAP.items():
        if any(kw in text_lower for kw in keywords):
            job_type = jtype
            break

    years_match = re.search(r"(\d+)\+?\s*years?", text_lower)
    years_exp = int(years_match.group(1)) if years_match else None

    meaningful_tokens = [
        t for t in tokens
        if t not in STOP_WORDS and len(t) > 2 and t.isalpha()
    ]

    return {
        "job_title": job_title,
        "skills": skills,
        "seniority": seniority,
        "job_type": job_type,
        "years_exp": years_exp,
        "keywords": meaningful_tokens[:10],
        "raw_text": user_text,
    }


FILLER_WORDS = {
    "find", "search", "looking", "want", "need", "show", "get", "look",
    "job", "jobs", "role", "roles", "position", "positions", "listing", "listings",
    "please", "can", "you", "me", "for", "a", "an", "the", "i",
    "with", "in", "on", "at", "and", "or", "title", "only",
    "linkedin", "indeed", "both",
}


def _clean_raw_input(raw: str) -> str:
    """Strip filler/meta words; preserve the user's actual search intent."""
    tokens = re.sub(r"[^\w\s+#.-]", " ", raw).split()
    cleaned = [t for t in tokens if t.lower(
    ) not in FILLER_WORDS and len(t) > 1]
    return " ".join(cleaned)


def extract_source_filter(text: str) -> str:
    """Return 'linkedin', 'indeed', or 'both' based on user message."""
    t = text.lower()
    has_linkedin = "linkedin" in t
    has_indeed = "indeed" in t
    if has_linkedin and not has_indeed:
        return "linkedin"
    if has_indeed and not has_linkedin:
        return "indeed"
    return "both"


def build_search_query(profile: dict) -> str:
    """Build a search query directly from the user's raw input.

    Raw text is always the primary source so niche/unrecognised terms
    (e.g. 'datadomain', 'system test') pass through verbatim.
    Structured extraction (job_title, seniority) is only used to
    augment when it adds real signal.
    """
    raw = profile.get("raw_text", "")
    base = _clean_raw_input(raw)

    # If structured extraction found a title not already present in base, prefer it
    title = profile.get("job_title", "")
    if title and title not in base.lower():
        base = title + (" " + base if base else "")

    # Prepend seniority if detected and not already in base
    seniority = profile.get("seniority", "any")
    if seniority not in ("any", None) and seniority not in base.lower():
        base = seniority + " " + base

    return base.strip() if base.strip() else "software engineer"


def score_job(job: dict, profile: dict) -> int:
    """Score a job listing by relevance to the user profile."""
    text = (
        (job.get("title") or "") + " " +
        (job.get("snippet") or "") + " " +
        (job.get("company") or "")
    ).lower()

    score = 0

    for skill in profile.get("skills", []):
        if skill in text:
            score += 3

    for kw in profile.get("keywords", []):
        if kw in text:
            score += 1

    if profile.get("job_title") and profile["job_title"] in text:
        score += 5

    if profile.get("seniority", "any") != "any":
        for kw in SENIORITY_MAP.get(profile["seniority"], []):
            if kw in text:
                score += 2
                break

    if profile.get("job_type", "any") != "any":
        for kw in JOB_TYPE_MAP.get(profile["job_type"], []):
            if kw in text:
                score += 2
                break

    if job.get("salary"):
        score += 1

    date = (job.get("date_posted") or "").lower()
    if "just posted" in date or "today" in date or "hour" in date:
        score += 2
    elif "day" in date and any(c.isdigit() for c in date):
        days = re.search(r"(\d+)\s*day", date)
        if days and int(days.group(1)) <= 3:
            score += 1

    if job.get("source") == "LinkedIn":
        score += 1

    return score


def rank_jobs(jobs: list[dict], profile: dict) -> list[dict]:
    """Sort jobs by relevance score descending."""
    for job in jobs:
        job["score"] = score_job(job, profile)
    return sorted(jobs, key=lambda j: j["score"], reverse=True)


def generate_agent_response(jobs: list[dict], profile: dict, query: str) -> str:
    """Generate a human-readable agent guidance message."""
    if not jobs:
        return (
            f"I searched both Indeed and LinkedIn for **{query}** in the Bay Area "
            "but didn't find results right now — both sites may be rate-limiting. "
            "Try again in a few seconds, or rephrase your request with different keywords."
        )

    indeed_count = sum(1 for j in jobs if j.get("source") == "Indeed")
    linkedin_count = sum(1 for j in jobs if j.get("source") == "LinkedIn")
    top = jobs[:3]

    source_str = f"{indeed_count} from Indeed, {linkedin_count} from LinkedIn"
    top_companies = ", ".join(set(j["company"]
                              for j in top if j["company"] != "N/A"))
    skill_str = ", ".join(profile.get("skills", [])[:4]
                          ) if profile.get("skills") else "your skills"
    seniority_str = f" ({profile['seniority']})" if profile.get(
        "seniority", "any") != "any" else ""

    msg_parts = [
        f"Found **{len(jobs)} Bay Area jobs** matching **{query}**{seniority_str} — {source_str}.",
    ]

    if top_companies:
        msg_parts.append(f"Top companies hiring: **{top_companies}**.")

    if profile.get("job_type") == "remote":
        remote_count = sum(
            1 for j in jobs
            if any(kw in (j.get("title", "") + j.get("snippet", "") + j.get("location", "")).lower()
                   for kw in ["remote", "wfh"])
        )
        msg_parts.append(f"{remote_count} listings mention remote/WFH.")

    if profile.get("skills"):
        msg_parts.append(
            f"Results are ranked by match to your skills: **{skill_str}**. "
            "Higher-scoring jobs appear first."
        )

    msg_parts.append(
        "You can refine: try typing *'only remote'*, *'more senior roles'*, "
        "*'startups only'*, or name a specific skill to narrow results."
    )

    return " ".join(msg_parts)
