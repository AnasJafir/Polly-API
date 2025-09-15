import threading
import time
import uuid
from typing import Optional

import requests
import uvicorn

from client import register_user
from main import app


def wait_for_server(url: str, timeout_seconds: float = 5.0) -> None:
    deadline = time.time() + timeout_seconds
    last_err: Optional[Exception] = None
    while time.time() < deadline:
        try:
            requests.get(url, timeout=0.5)
            return
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(0.1)
    if last_err:
        raise last_err


def main() -> None:
    host = "127.0.0.1"
    port = 8000
    base_url = f"http://{host}:{port}"

    config = uvicorn.Config(app=app, host=host, port=port, log_level="error")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    wait_for_server(base_url)

    username = f"user_{uuid.uuid4().hex[:8]}"
    result = register_user(base_url, username, "secret")
    print(result)

    server.should_exit = True
    thread.join(timeout=2)


if __name__ == "__main__":
    main()


