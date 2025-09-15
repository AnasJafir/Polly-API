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


def vote_on_poll(
    base_url: str,
    poll_id: int,
    option_id: int,
    access_token: str,
    timeout: float = 10.0,
) -> Dict[str, Any]:

    url = f"{base_url.rstrip('/')}/polls/{poll_id}/vote"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"option_id": option_id}

    response = requests.post(url, json=payload, headers=headers, timeout=timeout)

    if response.status_code == 401:

        raise PermissionError("Unauthorized: invalid or missing token")
    if response.status_code == 404:

        raise ValueError("Poll or option not found")

    response.raise_for_status()

    return response.json()


__all__.append("vote_on_poll")


def get_poll_results(
    base_url: str,
    poll_id: int,
    timeout: float = 10.0,
) -> Dict[str, Any]:

    url = f"{base_url.rstrip('/')}/polls/{poll_id}/results"
    response = requests.get(url, timeout=timeout)

    if response.status_code == 404:

        raise ValueError("Poll not found")

    response.raise_for_status()

    return response.json()


__all__.append("get_poll_results")


