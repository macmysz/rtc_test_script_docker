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
podman run -d --replace  --name rtc-tester-v2   -v /home/macmysz/data:/app/data:Z   -w /app   -e DELAY=600   -e PCNUM=X   --restart=unless-stopped   macmysz/ntp_rtc_logger_v2:latest

  ```
