"""
SK Hynix QA / Test Engineer coding practice
============================================

Scenario: You are given a semiconductor Final Test log (test_results.log).
Each line has fields separated by '|':

    timestamp | lot | wafer | die_x | die_y | test_name | bin | result | value

Your job (typical on-site interview task): parse the log and answer
common QA questions. Fill in the TODOs. Run:  python yield_exercise.py

Bins: bin 1 = PASS (good die). Any other bin = a specific failure category.

Tasks
-----
1. parse_log(path)         -> return a list of dicts (one per die).
2. overall_yield(records)  -> return pass % (good die / total die).
3. yield_by_lot(records)   -> return {lot: yield_percent}.
4. failure_pareto(records) -> return list of (bin, count) for FAILs,
                              sorted most-frequent first (a Pareto).
5. test_stats(records, test_name) -> return (mean, min, max) of `value`
                                     for a given test_name.

Bonus: which lot should QA investigate first, and why?
"""

from collections import Counter, defaultdict


def parse_log(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            # skip blank lines and comment lines starting with '#'
            if not line or line.startswith("#"):
                continue
            # TODO: split on '|', strip each field, build a dict, append it.
            # Suggested keys: timestamp, lot, wafer, die_x, die_y,
            #                 test_name, bin (int), result, value (float)
            pass
    return records


def overall_yield(records):
    # TODO: return percentage of records where result == "PASS"
    pass


def yield_by_lot(records):
    # TODO: return {lot: pass_percent} for each lot
    pass


def failure_pareto(records):
    # TODO: count FAIL records per bin, return list of (bin, count)
    #       sorted from most to least frequent.
    pass


def test_stats(records, test_name):
    # TODO: return (mean, min, max) of `value` for the given test_name
    pass


if __name__ == "__main__":
    recs = parse_log("test_results.log")
    print("Total die tested:", len(recs))
    print("Overall yield %:", overall_yield(recs))
    print("Yield by lot:", yield_by_lot(recs))
    print("Failure Pareto:", failure_pareto(recs))
    print("RETENTION stats (mean,min,max):", test_stats(recs, "RETENTION"))
