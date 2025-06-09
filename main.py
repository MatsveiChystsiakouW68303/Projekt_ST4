from collections import Counter
from processor import process_chunk
from visualizer import (
    plot_top_ips,
    plot_status_codes,
    plot_top_urls,
    plot_request_frequency
)
import multiprocessing


def read_in_chunks(filepath, chunk_size=10000):
    with open(filepath, 'r', encoding='utf-8') as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

if __name__ == "__main__":
    log_file = "logs/access.log"

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(process_chunk, read_in_chunks(log_file))

    total_ips = Counter()
    total_statuses = Counter()
    total_urls = Counter()
    total_methods = Counter()
    all_times = []

    for ip_c, st_c, url_c, times, method_c in results:
        total_ips.update(ip_c)
        total_statuses.update(st_c)
        total_urls.update(url_c)
        total_methods.update(method_c)
        all_times.extend(times)

    print("\n Top 5 adresów IP:")
    for ip, count in total_ips.most_common(5):
        print(f"{ip}: {count}")

    print("\n Częstotliwość kodów odpowiedzi:")
    for status, count in total_statuses.items():
        print(f"{status}: {count}")

    print("\n Top 5 adresów URL:")
    for url, count in total_urls.most_common(5):
        print(f"{url}: {count}")

    print("\n Typy zapytań HTTP:")
    for method, count in total_methods.items():
        print(f"{method}: {count}")

    # Wizualizacja danych
    plot_top_ips(total_ips)
    plot_status_codes(total_statuses)
    plot_top_urls(total_urls)
    plot_request_frequency(all_times)

    print("\n Wykresy zostały zapisane jako: top_ips.png, status_codes.png, top_urls.png, requests_over_time.png")
