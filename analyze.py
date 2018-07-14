import datetime
from pprint import pprint

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# First you have to remove first line and convert to UTF-8
InputFilename = 'submissions.log'

def main():
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
            this_time = datetime.datetime.strptime(parts[0].split(".")[0], "%Y-%m-%d %H:%M:%S")
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
            seen_times[this_id].append(this_time)
            seen_ups[this_id].append(this_ups)
            seen_scores[this_id].append(this_score)

    print(f"Found {len(created)} unique submissions")

    ax = plt.subplot()

    # Only show submissions created after a certain time ago
    # ago = datetime.timedelta(hours=20)
    # created = [x for x in created if (created[x] + ago > datetime.datetime.now())]

    # Only show submissions created since we started logging
    # beginning_of_log = min([x[0] for x in seen_times.values()])
    # created = [x for x in created if (created[x] > beginning_of_log)]

    # Only show big submissions
    # created = [x for x in created if len([s for s in seen_scores[x] if s > 5000]) > 0]

    print(f"After filtering, {len(created)} will be displayed")

    for id in created:
        plt.plot_date(seen_times[id], seen_ups[id], xdate=True, markersize=0.4)

    formatter = DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(formatter)

    # ax.set_ylim([0, 100])

    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()
