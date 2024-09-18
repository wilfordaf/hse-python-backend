import json
from typing import Any, Callable, Dict

from .errors import HTTPError, send_error
from .math_functions import factorial, fibonacci, mean


async def app(scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
    if scope["type"] != "http":
        return

    method: str = scope["method"]
    path: str = scope["path"]

    if path.startswith("/factorial") and method == "GET":
        await handle_factorial_request(scope, send)
        return

    if path.startswith("/fibonacci") and method == "GET":
        await handle_fibonacci_request(path, send)
        return

    if path.startswith("/mean") and method == "GET":
        await handle_mean_request(receive, send)
        return

    await send_error(send, HTTPError(404, {"error": "Not Found"}))


async def handle_factorial_request(scope: Dict[str, Any], send: Callable) -> None:
    query_string = scope["query_string"].decode()
    params = dict(param.split("=") for param in query_string.split("&") if "=" in param)
    n = params.get("n", 0)

    if not n:
        await send_error(send, HTTPError(422, {"error": "Unprocessable Entity"}))
        return

    try:
        int_n = int(n)
    except ValueError:
        await send_error(send, HTTPError(422, {"error": "Unprocessable Entity"}))
        return

    if int_n < 0:
        await send_error(send, HTTPError(400, {"error": "Bad Request"}))
        return

    result = {"result": factorial(int_n)}
    await send_json(send, result)
    return


async def handle_fibonacci_request(path, send) -> None:
    try:
        path_parts = path.split("/")
        n = int(path_parts[-1])
    except (ValueError, IndexError):
        await send_error(send, HTTPError(422, {"error": "Unprocessable Entity"}))
        return

    if n < 0:
        await send_error(send, HTTPError(400, {"error": "Bad Request"}))
        return

    result = {"result": fibonacci(n)}
    await send_json(send, result)
    return


async def handle_mean_request(receive, send) -> None:
    body = await read_body(receive)
    try:
        numbers = json.loads(body)
    except json.JSONDecodeError:
        await send_error(send, HTTPError(422, {"error": "Unprocessable Entity"}))
        return

    if not isinstance(numbers, list) or not all(isinstance(x, (int, float)) for x in numbers):
        await send_error(send, HTTPError(422, {"error": "Unprocessable Entity"}))
        return

    if len(numbers) == 0:
        await send_error(send, HTTPError(400, {"error": "Bad Request"}))
        return

    result = {"result": mean(numbers)}
    await send_json(send, result)
    return


async def send_json(send: Callable, data: Dict[str, Any], status: int = 200):
    body = json.dumps(data).encode("utf-8")
    headers = [(b"content-type", b"application/json")]
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": headers,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": body,
        }
    )


async def read_body(receive: Callable) -> bytes:
    body = b""

    while True:
        message = await receive()
        if message["type"] != "http.request":
            continue

        body += message.get("body", b"")
        if not message.get("more_body", False):
            break

    return body
