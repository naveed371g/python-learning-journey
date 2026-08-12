"""
==============================================================================
INTERVIEW PRACTICE: Reading & extracting info from an engineering log file
==============================================================================

THE SETUP (what an interviewer would hand you):

You are given a semiconductor test log 'test_results.log' with this format:
    timestamp | lot | wafer | die_x | die_y | test_name | bin | result | value

Lines starting with '#' are comments and should be skipped.

Below are the kinds of questions that get asked, from easy to hard.
Each function is one interview question. Read the docstring first, then the code.
==============================================================================
"""

from collections import Counter, defaultdict


# ----------------------------------------------------------------------------
# STEP 0: Read the file and turn each line into a clean dictionary (a "record")
# ----------------------------------------------------------------------------
# Almost every log-parsing interview starts here. If you can do this cleanly,
# every follow-up question becomes easy because you just loop over records.
def parse_log(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()                 # remove leading/trailing spaces + newline
            # skip blank lines and comments
            if not line or line.startswith("#"):
                continue
            # split on | and clean each field
            parts = [p.strip() for p in line.split("|")]
            ts, lot, wafer, dx, dy, test, bin_, result, value = parts  # unpack 9 fields
            records.append({
                "timestamp": ts,
                "lot": lot,
                "wafer": wafer,
                "die_x": int(dx),      # convert numbers from str -> int
                "die_y": int(dy),
                "test_name": test,
                "bin": int(bin_),
                "result": result,
                "value": float(value),  # value is a decimal -> float
            })
    return records


# ----------------------------------------------------------------------------
# Q1 (EASY): How many tests PASSED and how many FAILED?
# ----------------------------------------------------------------------------
# Skill tested: filtering + counting.
def count_pass_fail(records):
    passed = sum(1 for r in records if r["result"] == "PASS")
    failed = sum(1 for r in records if r["result"] == "FAIL")
    return passed, failed


# ----------------------------------------------------------------------------
# Q2 (EASY): What is the overall yield (percentage of PASS)?
# ----------------------------------------------------------------------------
# Skill tested: guarding against divide-by-zero + rounding.
def overall_yield(records):
    if not records:            # never divide by zero
        return 0.0
    passed = sum(1 for r in records if r["result"] == "PASS")
    return round(passed / len(records) * 100, 2)


# ----------------------------------------------------------------------------
# Q3 (MEDIUM): How many tests were run per lot?
# ----------------------------------------------------------------------------
# Skill tested: grouping with a dictionary. defaultdict(int) avoids KeyError.
def tests_per_lot(records):
    counts = defaultdict(int)
    for r in records:
        counts[r["lot"]] += 1
    return dict(counts)


# ----------------------------------------------------------------------------
# Q4 (MEDIUM): Which failure bins are most common? (Pareto of failures)
# ----------------------------------------------------------------------------
# Skill tested: Counter + only counting rows that match a condition.
def failure_bin_pareto(records):
    fails = Counter(r["bin"] for r in records if r["result"] == "FAIL")
    return fails.most_common()   # list of (bin, count) sorted high -> low


# ----------------------------------------------------------------------------
# Q5 (MEDIUM): What is the yield for EACH lot?
# ----------------------------------------------------------------------------
# Skill tested: two parallel dictionaries (total + passed), then combine.
def yield_by_lot(records):
    total = defaultdict(int)
    passed = defaultdict(int)
    for r in records:
        total[r["lot"]] += 1
        if r["result"] == "PASS":
            passed[r["lot"]] += 1
    return {lot: round(passed[lot] / total[lot] * 100, 2) for lot in total}


# ----------------------------------------------------------------------------
# Q6 (HARDER): For a given test_name, what's the average measured value?
# ----------------------------------------------------------------------------
# Skill tested: collecting values into a list, then averaging safely.
def average_value_by_test(records):
    buckets = defaultdict(list)
    for r in records:
        buckets[r["test_name"]].append(r["value"])
    return {name: round(sum(vals) / len(vals), 3) for name, vals in buckets.items()}


# ----------------------------------------------------------------------------
# Q7 (HARDER): Find the "worst" wafer (highest failure count).
# ----------------------------------------------------------------------------
# Skill tested: grouping by a key, then using max() with a key function.
def worst_wafer(records):
    fails = defaultdict(int)
    for r in records:
        if r["result"] == "FAIL":
            # a wafer is identified by lot + wafer
            key = (r["lot"], r["wafer"])
            fails[key] += 1
    if not fails:
        return None
    return max(fails, key=lambda k: fails[k])  # key with the biggest value


# ----------------------------------------------------------------------------
# RUN EVERYTHING (this is how you'd demo your answers to the interviewer)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    records = parse_log("test_results.log")

    print("Total records parsed:", len(records))

    passed, failed = count_pass_fail(records)
    print("\nQ1 - Pass/Fail:", passed, "passed,", failed, "failed")

    print("Q2 - Overall yield:", overall_yield(records), "%")

    print("Q3 - Tests per lot:", tests_per_lot(records))

    print("Q4 - Failure bin pareto:", failure_bin_pareto(records))

    print("Q5 - Yield by lot:", yield_by_lot(records))

    print("Q6 - Avg value by test:", average_value_by_test(records))

    print("Q7 - Worst wafer (lot, wafer):", worst_wafer(records))
