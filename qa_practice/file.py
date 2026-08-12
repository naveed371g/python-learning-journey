
from collections import Counter


def test(path):
    PASSnumber = 0
    with open(path) as file:
        for line in file:
            count = line.split()
            # print(count)
            if "LEAKAGE" in count and "FAIL" in count:
                PASSnumber += 1
                print(line)
                # print(PASSnumber)
    return PASSnumber


test1 = test("test_results.log")
print("Number of PASS ", test1)
