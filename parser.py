import re
from datetime import datetime
from collections import Counter

# Пример строки: 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s.*\[(?P<datetime>[^\]]+)\]\s"(?P<request>.*?)"\s(?P<status>\d+)'
)

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d{3})'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        ip = match.group("ip")
        method = match.group("method")
        url = match.group("url")
        status = match.group("status")
        dt_str = match.group("datetime")
        time = datetime.strptime(dt_str.split()[0], "%d/%b/%Y:%H:%M:%S")
        return ip, method, url, status, time
    return None

def parse_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

log_line_pattern = re.compile(
    r'(?P<ip>[\d.]+) - - \[(?P<time>[^\]]+)\] "(?P<method>\w+) (?P<url>[^ ]+) HTTP/\d\.\d" (?P<status>\d+)'
)

def parse_log_file(filename):
    ip_counter = Counter()
    status_counter = Counter()
    url_counter = Counter()
    time_list = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            match = log_line_pattern.match(line)
            if match:
                ip = match.group("ip")
                status = match.group("status")
                url = match.group("url")
                time_str = match.group("time")
                try:
                    time = datetime.strptime(time_str.split()[0], "%d/%b/%Y:%H:%M:%S")
                    time_list.append(time)
                except ValueError:
                    pass

                ip_counter[ip] += 1
                status_counter[status] += 1
                url_counter[url] += 1

    return ip_counter, status_counter, url_counter, time_list