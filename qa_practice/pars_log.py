# from github_projects.qa_practice.interview_log_parser import records


def test(path):
    records = []
    with open(path) as file:
        for line in file:
            line = line.strip()  # remove the space from line
            # do not line with # or there is nothing on line
            if not line or line.startswith("#"):
                continue
            parts = [p.strip()
                     for p in line.split("|")]  # use "|" as separator
            while len(parts) < 6:  # some of the line are less than 6 then use empty ""
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


test1 = test("test_run.log")
print(test1)


def result_summary(records):
    summary = {}
    for r in records:
        result = r["result"]          # "PASS", "FAIL", or "SKIP"
        print(result)
        if result not in summary:
            summary[result] = 0       # first time we see it, start at 0
            print(summary)
        summary[result] += 1          # count it
        print("summary is ", summary)
    return summary


records = test("test_run.log")
print("Total tests:", len(records))
print("\nQ1 - Result summary:", result_summary(records))
