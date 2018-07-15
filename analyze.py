import datetime
import pickle
from pprint import pprint
import random

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import (DAILY, HOURLY, DateFormatter, rrulewrapper, RRuleLocator)

regenerate_data = True

# First you have to remove first line and convert to UTF-8
InputFilename = 'submissions.log'
# InputFilename = 'submissions-small.log'

CreatedPickle    = "created.pickle"
SeenTimesPickle  = "seenTimes.pickle"
SeenUpsPickle    = "seenUps.pickle"
SeenScoresPickle = "seenScores.pickle"

def main():
    if regenerate_data:
        created = {}
        seen_times = {}
        seen_ups = {}
        seen_scores = {}

        with open(InputFilename, 'r') as f:
            for line in f:
                parts = [x for x in line.strip().split("\t")]
                if len(parts) != 5:
                    raise Exception(f"Unexpected data here: {line}")

                # this_time = int(parts[2][0:3])
                this_time = datetime.datetime.strptime(parts[0].split(".")[0], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=7)
                this_id = parts[1]
                this_created = datetime.datetime.fromtimestamp(float(parts[2]))
                this_ups = int(parts[3])
                this_score = int(parts[4])

                if this_id not in created:
                    created[this_id] = this_created
                    assert(this_id not in seen_times)
                    seen_times[this_id] = []
                    seen_ups[this_id] = []
                    seen_scores[this_id] = []

                assert(created[this_id] == this_created)

                if this_time < this_created + datetime.timedelta(hours=4):
                    seen_times[this_id].append(this_time)
                    seen_ups[this_id].append(this_ups)
                    seen_scores[this_id].append(this_score)

        with open(CreatedPickle, 'wb') as f:
            pickle.dump(created, f)
        with open(SeenTimesPickle, 'wb') as f:
            pickle.dump(seen_times, f)
        with open(SeenUpsPickle, 'wb') as f:
            pickle.dump(seen_ups, f)
        with open(SeenScoresPickle, 'wb') as f:
            pickle.dump(seen_scores, f)

    with open(CreatedPickle, 'rb') as f:
        created = pickle.load(f)
    with open(SeenTimesPickle, 'rb') as f:
        seen_times = pickle.load(f)
    with open(SeenUpsPickle, 'rb') as f:
        seen_ups = pickle.load(f)
    with open(SeenScoresPickle, 'rb') as f:
        seen_scores = pickle.load(f)

    print(f"Found {len(created)} unique submissions")

    ax = plt.subplot()

    # Only show submissions created since we started logging
    beginning_of_log = min([x[0] for x in seen_times.values() if len(x) > 0])
    created = [x for x in created if (created[x] > beginning_of_log)]

    # Only show submissions that reached thresh
    # thresh = 50
    # created = [x for x in created if len(seen_scores[x]) > 0 and max(seen_scores[x]) >= thresh]

    # Only show a random sample of submissions
    # proportion = 0.1
    # created = [x for x in created if random.uniform(0, 1) < proportion]

    print(f"After filtering, {len(created)} will be displayed")

    for id in created:
        plt.plot_date(seen_times[id], seen_ups[id], xdate=True, markersize=1, marker=".", linestyle="solid")

    rule = rrulewrapper(DAILY, interval=1)
    loc = RRuleLocator(rule)
    ax.xaxis.set_major_locator(loc)

    formatter = DateFormatter('%m/%d')
    ax.xaxis.set_major_formatter(formatter)

    ax.set_ylim([0, 500])

    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()
