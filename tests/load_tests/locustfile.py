import logging
import os
import subprocess

from locust import FastHttpUser, TaskSet, between, events, tag, task


class ApiLoadTest(TaskSet):
    TARGET_RPS = 5
    service_process: subprocess.Popen[bytes]

    @tag("api")
    @task
    def get_user(self):
        headers = {"Content-Type": "application/json"}
        params = {"username": "admin"}
        auth = ("admin", os.getenv("ADMIN_PASSWORD"))
        with self.client.post("/user-get", headers=headers, params=params, auth=auth, catch_response=True) as response:
            if response.status_code >= 400:
                response.failure("Запрос не прошёл")
            else:
                response.success()


class PredictUser(FastHttpUser):
    tasks = [ApiLoadTest]
    time = 1 / ApiLoadTest.TARGET_RPS
    wait_time = between(time, time)
    host = "http://localhost:8000"


@events.quitting.add_listener
def _(environment):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--api-target-rps", type=int, default=5, env_var="API_LOAD_TEST_TARGET_RPS")
