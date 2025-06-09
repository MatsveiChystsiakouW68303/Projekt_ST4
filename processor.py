from collections import Counter
from parser import parse_log_line
from datetime import datetime

def process_chunk(chunk):
    ip_counter = Counter()
    status_counter = Counter()
    url_counter = Counter()
    method_counter = Counter()
    timestamps = []

    for line in chunk:
        parsed = parse_log_line(line)
        if parsed:
            ip, method, url, status, time = parsed
            ip_counter[ip] += 1
            status_counter[status] += 1
            url_counter[url] += 1
            method_counter[method] += 1
            timestamps.append(time)

    return ip_counter, status_counter, url_counter, timestamps, method_counter
