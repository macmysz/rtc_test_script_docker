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