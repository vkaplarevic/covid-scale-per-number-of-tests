#! env python3

import sys
import matplotlib.pyplot as plt

LOCATION=2
DATE=3
NEW_CASES=5
NEW_TESTS=16
NEW_TESTS_SMOTHED=20


def print_header_indexes(h_raw):
    header = h_raw.split(",")
    header_nice = [str(c) + ":" + header[c] for c in  range(len(header))]
    print("\n".join(header_nice))


def main():
    dates = []
    new_cases = []
    new_cases_adjusted = []
    tested = []

    f = open(sys.argv[1], "r")
    country_code = sys.argv[2]

    #h = f.readline()
    #print_header_indexes(h)

    for line in f:
        data = line.split(",")

        new_tests = float(data[NEW_TESTS_SMOTHED]) if data[NEW_TESTS_SMOTHED] != "" and int(float(data[NEW_TESTS_SMOTHED])) != 0 else 0
        if new_tests == 0:
            continue

        dates.append(data[DATE])
        new_cases.append(float(data[NEW_CASES] if data[NEW_CASES] is not None and data[NEW_CASES] != "" else 0)) 
        tested.append(new_tests)
    f.close()

    # Adjust number of tests based on the last:
    if len(tested) == 0:
        print("No testing info available")
        return

    specific_day_tested = max(tested) if sys.argv[3] == "max" else tested[-1];
    for i in range(len(dates)):
        adjust_factor = specific_day_tested/tested[i] if tested[i] != 0 else 0
        new_cases_adjusted.append(new_cases[i] * adjust_factor)

    xticks=[dates[0], dates[int((0 + len(dates))/2)], dates[-1]]

    plt.subplot(131)
    plt.title("Cases Per Day(as reported)")
    plt.bar(dates, new_cases, color="blue")
    plt.xticks(xticks)
    
    plt.subplot(132)
    plt.title("Tests Per Day")
    plt.bar(dates, tested, color="blue")
    plt.xticks(xticks)

    plt.subplot(133)

    title_new_cases = "Cases Adjusted For The Number Of " + (
            "Tests On The Last Day"  if sys.argv[3] != "max" else "Maximum Tests Done"
    )
    plt.title(title_new_cases, color="red")
    plt.bar(dates, new_cases_adjusted, color="red")

    plt.suptitle("Covid Cases Per Day " + country_code + " Adjusted", color="red")
    plt.xticks(xticks)
    
    plt.show()

main()

