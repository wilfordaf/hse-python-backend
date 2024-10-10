![Tests](https://github.com/wilfordaf/hse-python-backend/actions/workflows/tests.yml/badge.svg)

### Homework 3

<ins>Grafana Dashboard</ins>

![dashboard](docs/monitoring/dashboard.png)

### Homework 4

<ins>Команда для запуска тестов</ins>

`docker exec -it service locust --api-target-rps 10 --headless -u 10 -r 1 --run-time 10m -f /root/src/tests/load_tests/locustfile.py`

<ins>Отчёт Locust</ins>

![dashboard](docs/load_test/locust_report.png)

<ins>Отчёт Grafana</ins>

![dashboard](docs/load_test/service_stats.png)
