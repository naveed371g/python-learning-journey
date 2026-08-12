"""
Reference solution for yield_exercise.py
Run:  python yield_solution.py
"""

from collections import Counter, defaultdict


def parse_log(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            ts, lot, wafer, dx, dy, test, bin_, result, value = parts
            records.append({
                "timestamp": ts,
                "lot": lot,
                "wafer": wafer,
                "die_x": int(dx),
                "die_y": int(dy),
                "test_name": test,
                "bin": int(bin_),
                "result": result,
                "value": float(value),
            })
    return records


def overall_yield(records):
    if not records:
        return 0.0
    passed = sum(1 for r in records if r["result"] == "PASS")
    return round(passed / len(records) * 100, 2)


def yield_by_lot(records):
    total = defaultdict(int)
    passed = defaultdict(int)
    for r in records:
        total[r["lot"]] += 1
        if r["result"] == "PASS":
            passed[r["lot"]] += 1
    return {lot: round(passed[lot] / total[lot] * 100, 2) for lot in total}


def failure_pareto(records):
    fails = Counter(r["bin"] for r in records if r["result"] == "FAIL")
    return fails.most_common()


def test_stats(records, test_name):
    vals = [r["value"] for r in records if r["test_name"] == test_name]
    if not vals:
        return (None, None, None)
    return (round(sum(vals) / len(vals), 3), min(vals), max(vals))


if __name__ == "__main__":
    recs = parse_log("test_results.log")
    print("Total die tested:", len(recs))
    print("Overall yield %:", overall_yield(recs))
    print("Yield by lot:", yield_by_lot(recs))
    print("Failure Pareto:", failure_pareto(recs))
    print("RETENTION stats (mean,min,max):", test_stats(recs, "RETENTION"))

    # Bonus: lowest-yield lot is the first investigation candidate.
    yields = yield_by_lot(recs)
    worst = min(yields, key=lambda lot: yields[lot])
    print(f"\nInvestigate first: {worst} (lowest yield at {yields[worst]}%)")
