from collections import Counter, defaultdict
from typing import Iterable

import pandas as pd

from access_logs.parse import parse


def count_by_minute_and_status(records: Iterable) -> dict[str, dict[str, int]]:
    """Count the number of records from each minute for each status code.

    The return value is a dictionary mapping each status code to a dictionary
    mapping each minute to the number of records with that status code from
    that minute. E.g.:
    {
        "200": {
            "2020-12-19T12:57:00+00:00": 1,
            "2020-12-19T12:58:00+00:00": 5,
        },
        "404": {
            "2020-12-19T14:03:00+00:00": 14,
        },
    }
    """
    counts = defaultdict(Counter)

    for record in records:
        fields = parse(record)
        if not fields:
            continue

        status = fields["status"]
        timestamp = fields["date"].replace(":", " ", 1) + " " + fields["timezone"]
        datetime = pd.to_datetime(timestamp).tz_convert("UTC").tz_localize(None)
        minute_rounded = datetime.floor(freq="min")
        timestr = minute_rounded.isoformat()

        counts[status][timestr] += 1

    return counts
