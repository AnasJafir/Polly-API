from typing import Any, Dict, Optional

import requests


def register_user(base_url: str, username: str, password: str, timeout: float = 10.0) -> Dict[str, Any]:

    url = f"{base_url.rstrip('/')}/register"
    payload = {"username": username, "password": password}

    response = requests.post(url, json=payload, timeout=timeout)

    if response.status_code == 400:

        raise ValueError("Username already registered")

    response.raise_for_status()

    return response.json()


__all__ = ["register_user"]


