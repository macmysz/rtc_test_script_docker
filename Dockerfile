# Używamy oficjalnego obrazu Pythona 3
FROM python:3.11-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki z lokalnego folderu do kontenera
COPY rtc_tester_v2.py requirements.txt /app/

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Tworzymy katalog na dane
RUN mkdir /data

# Domyślny punkt startowy
CMD ["python", "-u", "rtc_tester_v2.py"]
