import logging
import re
from typing import Generator, Iterable

combined_log_format_pattern = re.compile(
    r"(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?)"
    r" \[(?P<date>.*?)(?= ) (?P<timezone>.*?)\]"
    r' "(?P<request_method>\w*) (?P<path>(?:[^"\\]|\\.)*?)(?P<request_version> HTTP/.*)?"'
    r" (?P<status>\d*?) (?P<length>-|\d*)"
    r' "(?P<referrer>(?:[^"\\]|\\.)*?)" "(?P<user_agent>(?:[^"\\]|\\.)*?)"'
)


def parse(line: str) -> dict[str, str]:
    match = combined_log_format_pattern.match(line)
    if match:
        return match.groupdict()
    else:
        logging.warning(f"Could not parse line: {line}")
        return None


def parse_all(lines: Iterable) -> Generator[dict[str, str], None, None]:
    for line in lines:
        parsed = parse(line)
        if parsed:
            yield parsed
