import matplotlib.pyplot as plt
from collections import Counter

def plot_top_ips(ip_counter, top_n=5):
    top = ip_counter.most_common(top_n)
    if not top:
        print("Nie ma danych do wyświetlania adresów IP.")
        return

    labels, values = zip(*top)

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color="skyblue")
    plt.title("Najczęściej występujące adresy IP")
    plt.xlabel("Adres IP")
    plt.ylabel("Liczba żądań")
    plt.tight_layout()
    plt.savefig("top_ips.png")
    plt.close()

def plot_status_codes(status_counter):
    if not status_counter:
        print("Brak danych do wyświetlania kodów odpowiedzi.")
        return

    labels = list(status_counter.keys())
    sizes = list(status_counter.values())

    # Usuwamy zera
    filtered = [(l, s) for l, s in zip(labels, sizes) if s > 0]
    if not filtered:
        print("Brak istotnych danych do wykresu kołowego.")
        return

    labels, sizes = zip(*filtered)

    # Generujemy podpisy typu: "kod (n%)"
    def make_autopct(sizes):
        def autopct(pct):
            total = sum(sizes)
            count = int(round(pct * total / 100.0))
            return f"{count} żądań\n({pct:.1f}%)"
        return autopct

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct=make_autopct(sizes),
        startangle=100,
        labeldistance=1.15,
        pctdistance=0.75,
        textprops=dict(color="black", fontsize=10)
    )

    plt.title("Rozkład kodów odpowiedzi HTTP")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("status_codes.png")
    plt.close()

def plot_top_urls(url_counter, top_n=5):
    top = url_counter.most_common(top_n)
    if not top:
        print("Brak danych do wyświetlenia adresów URL.")
        return

    labels, values = zip(*top)

    plt.figure(figsize=(10, 5))
    plt.barh(labels, values, color="lightgreen")
    plt.title("Najczęściej odwiedzane adresy URL")
    plt.xlabel("Liczba żądań")
    plt.ylabel("Adres URL")
    plt.tight_layout()
    plt.savefig("top_urls.png")
    plt.close()

def plot_request_frequency(time_list):
    if not time_list:
        print("Brak danych o czasie żądań.")
        return

    # Grupowanie według minut
    times_per_minute = [dt.replace(second=0) for dt in time_list]
    time_counter = Counter(times_per_minute)

    # Sortowanie po czasie
    sorted_items = sorted(time_counter.items())
    times, counts = zip(*sorted_items)

    plt.figure(figsize=(10, 5))
    plt.plot(times, counts, marker="o", linestyle="-", color="orange")
    plt.title("Liczba żądań w czasie")
    plt.xlabel("Czas")
    plt.ylabel("Liczba żądań")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("requests_over_time.png")
    plt.close()
