from datetime import datetime
import time
import ntplib
import csv
import os
import matplotlib.pyplot as plt


#test time
client = ntplib.NTPClient()
def time_test(retries=5, delay=10):
    for attempt in range(1, retries + 1):
        try:
            response = client.request('pool.ntp.org', version=3)
            ntp_time = datetime.fromtimestamp(response.tx_time)
            rtc_time = datetime.now()
            return rtc_time, ntp_time
        except Exception as e:
            print(f"[{attempt}/{retries}] ERROR NTP: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("Too many tries - can't connect to NTP server")
                return None, None

#format time
def time_format(time_in):
    time_formatted = time_in.strftime("%H:%M:%S") + f".{time_in.microsecond // 1000:03d}"
    return time_formatted

#get delta
def get_delta(time1_in, time2_in):
    delta_time_ms = (time1_in - time2_in).total_seconds() * 1000
    return round(delta_time_ms, 3)

#get date
def get_date():
    date = datetime.now().strftime("%d/%m/%Y")
    return date

#print plot
def plot_from_csv(csv_file, output_svg="plot.svg"):
    timestamps = []
    delta = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date_str = row['RTC_Date']
                time_str = row['RTC_Time']
                delta_val = float(row['Delta[ms]'])
                dt_str = f"{date_str} {time_str}"
                dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S.%f")
                timestamps.append(dt)
                delta.append(delta_val)
            except (ValueError, KeyError):
                continue

    if not timestamps or not delta:
        print("Brak danych do wyświetlenia wykresu.")
        return

    first_date = timestamps[0].strftime("%d/%m/%Y %H:%M:%S")
    last_date = timestamps[-1].strftime("%d/%m/%Y %H:%M:%S")
    min_delta = min(delta)
    max_delta = max(delta)

    plt.figure(figsize=(12,6))
    plt.axhline(0, color='red', linewidth=1.5, zorder=0)
    plt.plot(
        timestamps, delta,
        marker='o',
        markersize=1,
        linewidth=0.8,
        color='blue',
        linestyle='--',
        zorder=5
    )
    plt.title(f"Delta czasu RTC vs NTP [wolf-dev-rtc{pc_num}]")
    plt.xlabel("Data i godzina (RTC)")
    plt.ylabel("Delta [ms]")
    plt.grid(True)
    plt.xticks(rotation=45)

    # Tekst z informacjami (ustawiamy w rogu wykresu)
    info_text = (
        f"Pierwszy pomiar: {first_date}\n"
        f"Ostatni pomiar: {last_date}\n"
        f"Min delta: {min_delta:.3f} ms\n"
        f"Max delta: {max_delta:.3f} ms"
    )
    plt.gca().text(
        0.02, 0.98, info_text,
        transform=plt.gca().transAxes,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )

    plt.tight_layout()
    plt.savefig(output_svg)
    plt.close()




#-----*-----*-----*-----

delay = int(os.getenv("DELAY", 6000))
print(f"Delay set to: {round(delay/60, 3)}min")
pc_num = int(os.getenv("PCNUM", 1))
print(f"Runs on: wolf-dev-rtc{pc_num}")


csv_name = f"data/rtc-test-data_wolf-dev-rtc{pc_num}.csv"
svg_name = f"data/rtc-test-data_wolf-dev-rtc{pc_num}.svg"
lp = 0
#create new csv or data if not present
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(csv_name):

    with open(csv_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["LP", "RTC_Date", "RTC_Time", "NTP_Time", "Delta[ms]"])

else: #carry lp if script stops
    with open(csv_name, mode='r') as file:
        reader = list(csv.reader(file))
        data_rows = [row for row in reader if row and row[0].isdigit()]
        if data_rows:
            last_row = data_rows[-1]
            lp = int(last_row[0]) + 1
        else:
            lp = 0

#save to csv

while True:

    rtc_time1, ntp_time1 = time_test()
    if rtc_time1 and ntp_time1:
        delta_time = get_delta(rtc_time1, ntp_time1)
        row = [lp, get_date(), time_format(rtc_time1), time_format(ntp_time1), delta_time]

        print(row)
        with open(csv_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        lp+=1
        plot_from_csv(csv_name, svg_name)
    time.sleep(delay)

