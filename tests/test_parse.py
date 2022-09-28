from access_logs.parse import parse, parse_all

TYPICAL_LOG_LINE = (
    "123.66.150.17 - - [12/Aug/2010:02:45:59 +0000] "
    '"POST /wordpress3/wp-admin/admin-ajax.php HTTP/1.1" 200 2 '
    '"http://www.example.com/wordpress3/wp-admin/post-new.php" '
    '"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) '
    'AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.25 Safari/534.3"'
)

# Many of these were (real) examples that caused problems while writing the
# parsing regex.
EXAMPLE_LOG_LINES = [
    r'1.1.1.2 - - [11/Nov/2016:03:04:55 +0100] "GET /" 200 83 "-" "-"',
    r'127.0.0.1 - - [11/Nov/2016:14:24:21 +0100] "GET /uno dos" 404 298 "-" "-"',
    r'127.0.0.1 - - [11/Nov/2016:14:23:37 +0100] "GET /uno dos HTTP/1.0" 404 298 "-" "-"',
    r'1.1.1.1 - - [11/Nov/2016:00:00:11 +0100] "GET /icc HTTP/1.1" 302 - "-" "-"',
    r'1.1.1.1 - - [11/Nov/2016:00:00:11 +0100] "GET /icc/ HTTP/1.1" 302 - "-" "-"',
    r'157.48.153.185 - - [19/Dec/2020:14:08:08 +0100] "GET /favicon.ico HTTP/1.1" 404 217 "http://www.almhuette-raith.at/apache-log/access.log" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"',
    r'84.17.45.105 - - [02/May/2021:11:46:27 +0200] "GET /index.php?format=feed&type=\" HTTP/1.1" 200 3730 "-" "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"',
    r'84.17.45.105 - - [02/May/2021:11:46:27 +0200] "GET /favicon.ico HTTP/1.1" 404 217 "http://www.almhuette-raith.at/apache-log/access.log" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"',
    r'217.182.78.180 - - [28/Dec/2020:22:15:10 +0100] "GET /apache-log/error.log HTTP/1.1" 304 - "-" "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"',
    r'170.83.0.226 - - [18/Apr/2022:23:42:27 +0200] "get / HTTP/1.1" 200 10479 "-" "Mozilla/5.00 (Nikto/2.1.5) (Evasions:None) (Test:000445)"',
]


def test_parse_typical():
    fields = parse(TYPICAL_LOG_LINE)
    assert fields["ip"] == "123.66.150.17"
    assert fields["remote_log_name"] == "-"
    assert fields["userid"] == "-"
    assert fields["date"] == "12/Aug/2010:02:45:59"
    assert fields["timezone"] == "+0000"
    assert fields["request_method"] == "POST"
    assert fields["path"] == "/wordpress3/wp-admin/admin-ajax.php"
    assert fields["request_version"] == " HTTP/1.1"
    assert fields["status"] == "200"
    assert fields["length"] == "2"
    assert fields["user_agent"] == (
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) "
        "AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.25 Safari/534.3"
    )


def test_parse_malformed(capsys):
    assert parse("foo bar baz") is None


def test_parse_all():
    for line in EXAMPLE_LOG_LINES:
        assert parse(line) is not None
