#!/usr/bin/env python3
"""Smoke-test the four Lab 4 API URLs against a running server."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Check:
    name: str
    method: str
    path: str
    expected_statuses: frozenset[int]
    payload: dict[str, Any] | None = None


CHECKS = (
    Check("health", "GET", "/health", frozenset({200})),
    Check(
        "chat",
        "POST",
        "/v1/chat",
        frozenset({200}),
        {"message": "Thư viện ở đâu?"},
    ),
    Check(
        "feedback",
        "POST",
        "/v1/feedback",
        frozenset({200, 201, 202}),
        {
            "message_id": "url-test-message",
            "rating": 5,
            "comment": "URL smoke test",
        },
    ),
)


def _request(check: Check, base_url: str, timeout: float) -> tuple[int, str]:
    data = json.dumps(check.payload).encode() if check.payload is not None else None
    request = Request(
        base_url.rstrip("/") + check.path,
        data=data,
        method=check.method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310
            return response.status, response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--city", default="Ho Chi Minh City")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    weather_path = "/v1/weather?" + urlencode({"city": args.city})
    checks = CHECKS + (
        Check("weather", "GET", weather_path, frozenset({200})),
    )
    failures = 0

    for check in checks:
        try:
            status, body = _request(check, args.base_url, args.timeout)
        except (URLError, TimeoutError) as exc:
            failures += 1
            print(f"FAIL {check.name}: {exc}", file=sys.stderr)
            continue

        if status not in check.expected_statuses:
            failures += 1
            expected = ", ".join(map(str, sorted(check.expected_statuses)))
            print(
                f"FAIL {check.name}: expected {expected}, got {status}; body={body[:200]}",
                file=sys.stderr,
            )
        else:
            print(f"PASS {check.name}: HTTP {status}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
