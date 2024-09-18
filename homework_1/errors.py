import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Dict


@dataclass
class HTTPError:
    status_code: int
    body: Dict[str, str]


async def send_error(send: Callable, error: HTTPError):
    await send(
        {
            "type": "http.response.start",
            "status": error.status_code,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(error.body).encode("utf-8"),
        }
    )
