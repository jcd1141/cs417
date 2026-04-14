"""Lab 20: Build the Other Side — Client

Client functions that talk to your FastAPI server. Each task adds
a new function that handles a more realistic scenario.
"""

import requests
import time


def submit(student: str, lab: int, base_url: str = "http://localhost:8000") -> dict:
    """Task 1: Submit a grading request and return the result.

    POST to {base_url}/grade with {"student": student, "lab": lab}.
    Raise RuntimeError if the status code is not 200.
    Return the response as a dictionary.
    """
    # TODO: Implement
    response = requests.post(
        f"{base_url}/grade",
        json={"student": student, "lab": lab},
    )

    if response.status_code != 200:
        raise RuntimeError(f"Request failed with status code {response.status_code}")

    return response.json()


def submit_with_retry(
    student: str,
    lab: int,
    base_url: str = "http://localhost:8000",
    timeout: float = 2,
    max_retries: int = 3,
) -> dict:
    """Task 2: Submit with timeout and retry logic.

    POST to /grade with {"student": student, "lab": lab, "slow": True}.
    Use the timeout parameter in requests.post().
    On requests.exceptions.Timeout, retry up to max_retries times.
    Raise RuntimeError("all retries failed") if every attempt times out.
    Return the response dictionary on success.
    """
    # TODO: Implement
    for _ in range(max_retries):
        try:
            response = requests.post(
                f"{base_url}/grade",
                json={"student": student, "lab": lab, "slow": True},
                timeout=timeout,
            )

            if response.status_code != 200:
                raise RuntimeError(f"Request failed with status code {response.status_code}")

            return response.json()

        except requests.exceptions.Timeout:
            pass

    raise RuntimeError("all retries failed")


def submit_idempotent(
    student: str,
    lab: int,
    base_url: str = "http://localhost:8000",
    timeout: float = 2,
    max_retries: int = 3,
) -> dict:
    submission_id = f"{student}-lab{lab}"
    """Task 3: Submit with an idempotency key.

    Same as submit_with_retry, but include a stable submission_id
    in the request body: f"{student}-lab{lab}"
    """
    # TODO: Implement
    for _ in range(max_retries):
        try:
            response = requests.post(
                f"{base_url}/grade",
                json={
                    "student": student,
                    "lab": lab,
                    "slow": True,
                    "submission_id": submission_id
                },
                timeout=timeout,
            )

            if response.status_code != 200:
                raise RuntimeError(f"Request failed with status code {response.status_code}")

            return response.json()

        except requests.exceptions.Timeout:
            pass

    raise RuntimeError("all retries failed")


def submit_async(
    student: str,
    lab: int,
    base_url: str = "http://localhost:8000",
    poll_interval: float = 0.5,
    max_polls: int = 20,
) -> dict:
    submission_id = f"{student}-lab{lab}"

    response = requests.post(
        f"{base_url}/grade-async",
        json={
            "student": student,
            "lab": lab,
            "submission_id": submission_id
        }
    )

    if response.status_code != 202:
        raise RuntimeError(f"Request failed with status code {response.status_code}")

    job_id = response.json()["job_id"]

    for _ in range(max_polls):
        poll_response = requests.get(f"{base_url}/grade-jobs/{job_id}")
        data = poll_response.json()

        if data["status"] == "complete":
            return data["result"]

        time.sleep(poll_interval)

    raise RuntimeError("polling timed out")

# ---------------------------------------------------------------------------
# Bonus Task 5: The Smart Client
# ---------------------------------------------------------------------------


class SmartClient:
    """A client that tries sync first and falls back to async.

    Usage:
        client = SmartClient(base_url="http://localhost:8000")
        result = client.submit("alice", 19)
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 2):
        # TODO: Implement
        pass

    def submit(self, student: str, lab: int) -> dict:
        """Submit a grading request. Tries sync first, falls back to async."""
        # TODO: Implement
        pass