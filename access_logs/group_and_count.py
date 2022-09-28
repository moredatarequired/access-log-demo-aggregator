from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Union

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


def aggregate_logfile(src: Path, dest_root: Path) -> None:
    """Aggregate an access log file and write the summary to CSV.

    The access records from `src` will be counted by minute and by status code
    and a CSV file for each status code will be written to `dest_root`.

    I.e., if the file `src` contains the single record:
    ```
    1.1.1.2 - - [11/Nov/2016:03:04:55 +0100] "GET /" 200 83 "-" "-"
    ```
    then the file `dest_root/200.csv` will contain the header and single line:
    ```
    timestamp,count
    2016-11-11T02:04:00,1
    ```
    """
    dest_root.mkdir(exist_ok=True, parents=True)

    with src.open() as f:
        counts = count_by_minute_and_status(f)

    for status, counts_by_minute in counts.items():
        dest = dest_root / f"{status}.csv"
        with dest.open("w") as f:
            f.write("timestamp,count")
            for minute, count in counts_by_minute.items():
                f.write(f"{minute},{count}")


def aggregate_from_dir(src_root: Union[str, Path], dest_root: Union[str, Path]) -> None:
    """Aggregate all access log files in `src_root` and write the summaries to CSV.

    For each file `src_root/**/<name>.log` a directory `dest_root/**/<name>` will be
    created and the file `dest_root/<name>/<status>.csv` will be created for
    each status code `status` present in the log file.
    """
    src_root = Path(src_root)
    dest_root = Path(dest_root)

    for src in src_root.glob("**/*.log"):
        dest = dest_root / src.relative_to(src_root).parent / src.stem
        print(src, dest)
        aggregate_logfile(src, dest)