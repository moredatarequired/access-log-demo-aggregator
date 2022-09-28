from access_logs.group_and_count import count_by_minute_and_status

EXAMPLE_LOG_LINES = [
    '1.1.1.2 - - [11/Nov/2016:03:04:55 +0100] "GET /" 200 83 "-" "-"',
    '127.0.0.1 - - [11/Nov/2016:14:24:21 +0100] "GET /uno dos" 404 298 "-" "-"',
    '127.0.3.1 - - [11/Nov/2016:14:23:37 +0100] "GET /uno dos HTTP/1.0" 404 298 "-" "-"',
    '1.1.1.1 - - [11/Nov/2016:00:00:11 +0100] "GET /icc HTTP/1.1" 302 - "-" "-"',
    '4.4.4.4 - - [10/Nov/2016:23:00:04 +0000] "GET /icc HTTP/1.1" 302 - "-" "-"',
]


def test_count_by_minute_and_status():
    counts = count_by_minute_and_status(EXAMPLE_LOG_LINES)
    # Note: we expect the timezone to be localized to UTC and removed, which
    # will alter the time (and possibly the day) of the timestamp.
    assert counts == {
        "200": {"2016-11-11T02:04:00": 1},
        "404": {"2016-11-11T13:24:00": 1, "2016-11-11T13:23:00": 1},
        "302": {"2016-11-10T23:00:00": 2},
    }
