"""
==============================================================================
INTERVIEW PRACTICE: Parsing a QA / software test-automation run log
==============================================================================

THE SETUP (what an interviewer would hand you):

You are given 'test_run.log' from an automated test run (think pytest / JUnit /
Selenium output flattened into one line per test). Format:

    timestamp | suite | test_name | result | duration_ms | message

  - result is one of: PASS, FAIL, SKIP
  - message is empty for PASS, and holds the error/reason for FAIL and SKIP
  - lines starting with '#' are comments -> skip them

These are the questions a QA/SDET interviewer actually asks, easy -> hard.
Read each docstring, try it yourself, then compare with the code.
==============================================================================
"""

from collections import Counter, defaultdict


# ----------------------------------------------------------------------------
# STEP 0: Read the file and turn each line into a clean "record" dict.
# ----------------------------------------------------------------------------
# If you nail this, every follow-up is just a loop over records.
def parse_log(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()                  # drop newline + edge spaces
            if not line or line.startswith("#"):  # skip blanks and comments
                continue
            parts = [p.strip() for p in line.split("|")]  # split + clean each field
            # message may be missing -> pad the list so unpacking never crashes
            while len(parts) < 6:
                parts.append("")
            ts, suite, name, result, duration, message = parts
            records.append({
                "timestamp": ts,
                "suite": suite,
                "test_name": name,
                "result": result,
                "duration_ms": int(duration),   # str -> int
                "message": message,
            })
    return records


# ----------------------------------------------------------------------------
# Q1 (EASY): Give a summary count of PASS / FAIL / SKIP.
# ----------------------------------------------------------------------------
# Skill: counting by category. Counter does it in one line.
def result_summary(records):
    return dict(Counter(r["result"] for r in records))


# ----------------------------------------------------------------------------
# Q2 (EASY): What is the pass rate (%)?  (PASS out of PASS+FAIL, ignoring SKIP)
# ----------------------------------------------------------------------------
# Skill: careful denominator + divide-by-zero guard. Interviewers LOVE this
# detail: skipped tests usually should NOT count against your pass rate.
def pass_rate(records):
    passed = sum(1 for r in records if r["result"] == "PASS")
    run = sum(1 for r in records if r["result"] in ("PASS", "FAIL"))
    if run == 0:
        return 0.0
    return round(passed / run * 100, 2)


# ----------------------------------------------------------------------------
# Q3 (EASY/MEDIUM): List the names of all failing tests.
# ----------------------------------------------------------------------------
# Skill: filtering into a list. This is the "what actually broke?" question.
def failed_tests(records):
    return [r["test_name"] for r in records if r["result"] == "FAIL"]


# ----------------------------------------------------------------------------
# Q4 (MEDIUM): How many tests passed/failed in EACH suite?
# ----------------------------------------------------------------------------
# Skill: grouping. Nested dict keyed by suite -> Counter of results.
def results_by_suite(records):
    suites = defaultdict(Counter)
    for r in records:
        suites[r["suite"]][r["result"]] += 1
    return {suite: dict(counts) for suite, counts in suites.items()}


# ----------------------------------------------------------------------------
# Q5 (MEDIUM): Group failures by error TYPE (the part before the first ':').
# ----------------------------------------------------------------------------
# Skill: light string parsing. Turns raw messages into a Pareto of root causes,
# e.g. AssertionError vs TimeoutError -> tells you if it's a bug or flakiness.
def failure_types(records):
    types = Counter()
    for r in records:
        if r["result"] == "FAIL" and r["message"]:
            error_type = r["message"].split(":")[0].strip()  # "TimeoutError: ..." -> "TimeoutError"
            types[error_type] += 1
    return types.most_common()


# ----------------------------------------------------------------------------
# Q6 (MEDIUM/HARD): Find the slowest N tests (performance regression hunting).
# ----------------------------------------------------------------------------
# Skill: sorting by a field with a key function + slicing the top N.
def slowest_tests(records, n=3):
    ordered = sorted(records, key=lambda r: r["duration_ms"], reverse=True)
    return [(r["test_name"], r["duration_ms"]) for r in ordered[:n]]


# ----------------------------------------------------------------------------
# Q7 (HARD): Which suite is the "worst" (highest failure rate)?
# ----------------------------------------------------------------------------
# Skill: combine grouping + a computed ratio + max() with a key function.
def worst_suite(records):
    total = defaultdict(int)
    failed = defaultdict(int)
    for r in records:
        total[r["suite"]] += 1
        if r["result"] == "FAIL":
            failed[r["suite"]] += 1
    if not total:
        return None
    rates = {s: failed[s] / total[s] for s in total}
    worst = max(rates, key=lambda s: rates[s])
    return worst, round(rates[worst] * 100, 2)


# ----------------------------------------------------------------------------
# RUN EVERYTHING (how you'd demo your answers live)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    records = parse_log("test_run.log")

    print("Total tests:", len(records))
    print("\nQ1 - Result summary:", result_summary(records))
    print("Q2 - Pass rate (excl. SKIP):", pass_rate(records), "%")
    print("Q3 - Failed tests:", failed_tests(records))
    print("Q4 - Results by suite:", results_by_suite(records))
    print("Q5 - Failure types:", failure_types(records))
    print("Q6 - Slowest tests:", slowest_tests(records, 3))
    print("Q7 - Worst suite (name, fail%):", worst_suite(records))
