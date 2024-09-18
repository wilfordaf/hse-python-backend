import subprocess
import time
from pathlib import Path

import pytest
import requests

HOST = "localhost"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"
SCRIPT_PATH = Path(__file__).parents[1].resolve() / "homework_1/bin/run_app.sh"
print(SCRIPT_PATH)


@pytest.fixture(scope="session", autouse=True)
def app_runner():
    process = subprocess.Popen(["/bin/bash", SCRIPT_PATH.as_posix()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)

    try:
        response = requests.get(BASE_URL)
        if response.status_code not in {200, 404}:
            process.terminate()
            raise RuntimeError(f"Failed to start the app, unexpected status code: {response.status_code}")
    except requests.ConnectionError as e:
        process.terminate()
        raise RuntimeError("Failed to connect to the app on localhost:8000") from e

    yield

    process.terminate()
    process.wait()
