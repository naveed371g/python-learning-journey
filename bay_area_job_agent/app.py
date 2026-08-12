import logging
import threading
from flask import Flask, render_template, request, jsonify, session

from nlp_agent import extract_profile, build_search_query, rank_jobs, generate_agent_response, extract_source_filter, _clean_raw_input
from scraper import scrape_jobs

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "bay-area-job-agent-secret-2024"

_search_cache: dict[str, list[dict]] = {}
_search_lock = threading.Lock()

WELCOME_MESSAGE = (
    "Hi! I'm your Bay Area Job Search Agent. "
    "Tell me what kind of role you're looking for — include your skills, "
    "experience level, and whether you prefer remote/hybrid/onsite. "
    "For example: *'I'm a senior Python backend engineer looking for remote roles at startups'* "
    "or *'Data scientist with 3 years experience, open to hybrid in SF'*."
)

INTAKE_FIELDS = ["job_title", "skills", "seniority", "job_type"]


def _profile_is_complete(profile: dict) -> bool:
    """True when we have enough to form a meaningful search query."""
    raw = profile.get("raw_text", "")
    return bool(profile.get("job_title") or profile.get("skills") or _clean_raw_input(raw))


def _follow_up_question(profile: dict):
    if not profile.get("job_title") and not profile.get("skills"):
        return (
            "Could you be a bit more specific? What role or tech stack are you targeting? "
            "For example: *'Python developer'*, *'ML engineer'*, *'frontend with React'*."
        )
    if profile.get("seniority") == "any" and not profile.get("years_exp"):
        return (
            "What experience level are you? "
            "*(Junior / Mid-level / Senior / Staff / Manager)*"
        )
    return None


@app.route("/")
def index():
    session.clear()
    session["profile"] = {}
    session["history"] = [{"role": "agent", "text": WELCOME_MESSAGE}]
    return render_template("index.html", welcome=WELCOME_MESSAGE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = (data.get("message") or "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    history = session.get("history", [])
    existing_profile = session.get("profile", {})

    history.append({"role": "user", "text": user_msg})

    new_profile = extract_profile(user_msg)
    merged = {**existing_profile}
    # Always update raw_text with the latest message so query reflects current intent
    merged["raw_text"] = user_msg
    if new_profile["job_title"]:
        merged["job_title"] = new_profile["job_title"]
    if new_profile["skills"]:
        merged["skills"] = list(
            set(existing_profile.get("skills", []) + new_profile["skills"]))
    if new_profile["seniority"] != "any":
        merged["seniority"] = new_profile["seniority"]
    if new_profile["job_type"] != "any":
        merged["job_type"] = new_profile["job_type"]
    if new_profile["years_exp"]:
        merged["years_exp"] = new_profile["years_exp"]

    # Detect if user specified a source (linkedin / indeed)
    merged["source_filter"] = extract_source_filter(user_msg)

    merged.setdefault("job_title", "")
    merged.setdefault("seniority", "any")
    merged.setdefault("job_type", "any")
    merged.setdefault("skills", [])
    merged.setdefault("keywords", [])

    session["profile"] = merged

    if not _profile_is_complete(merged):
        follow_up = _follow_up_question(merged)
        agent_reply = follow_up or (
            "Got it! Tell me more about your target role or key skills so I can search effectively."
        )
        history.append({"role": "agent", "text": agent_reply})
        session["history"] = history
        return jsonify({"reply": agent_reply, "jobs": [], "searching": False})

    query = build_search_query(merged)
    cache_key = query.lower().strip()

    source_filter = merged.get("source_filter", "both")
    if source_filter == "linkedin":
        source_str = "LinkedIn"
    elif source_filter == "indeed":
        source_str = "Indeed"
    else:
        source_str = "Indeed + LinkedIn"

    agent_thinking = (
        f"Searching **{source_str}** for *'{query}'* in the Bay Area... "
        "This takes 20-40 seconds while I scrape the site(s)."
    )
    history.append({"role": "agent", "text": agent_thinking})
    session["history"] = history

    return jsonify({
        "reply": agent_thinking,
        "jobs": [],
        "searching": True,
        "query": query,
        "source_filter": source_filter,
    })


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = (data.get("query") or "").strip()
    profile = session.get("profile", {})

    if not query:
        return jsonify({"error": "No query provided"}), 400

    cache_key = query.lower().strip()
    with _search_lock:
        if cache_key in _search_cache:
            cached = _search_cache[cache_key]
            ranked = rank_jobs(list(cached), profile)
            reply = generate_agent_response(ranked, profile, query)
            return jsonify({"reply": reply, "jobs": ranked[:25]})

    source_filter = data.get("source_filter") or session.get(
        "profile", {}).get("source_filter", "both")
    logger.info(
        f"Starting scrape for query: '{query}' source: {source_filter}")
    jobs = scrape_jobs(query, max_per_source=15, source_filter=source_filter)
    ranked = rank_jobs(jobs, profile)

    with _search_lock:
        _search_cache[cache_key] = list(ranked)

    reply = generate_agent_response(ranked, profile, query)

    history = session.get("history", [])
    history.append({"role": "agent", "text": reply})
    session["history"] = history

    return jsonify({"reply": reply, "jobs": ranked[:25]})


@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    session["profile"] = {}
    session["history"] = [{"role": "agent", "text": WELCOME_MESSAGE}]
    with _search_lock:
        _search_cache.clear()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
