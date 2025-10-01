# rtc_test_script_docker



* Run docker compose
```
PCNUM=X docker-compose up --build -d
```

optionali set delay in seconds
```
DELAY=Y PCNUM=X docker-compose up --build -d
```

* Remove old data
```
sudo rm -rf /home/macmysz/data/*
```

* Run podman
```
PCNUM=X
podman run -d \
  --name rtc-tester-v2 \
  -v .:/app \
  -v /home/macmysz/data:/app/data \
  -w /app \
  -e DELAY=${DELAY} \
  -e PCNUM=${PCNUM} \
  --restart=unless-stopped \
  macmysz/ntp_rtc_logger_v2:latest
  ```
