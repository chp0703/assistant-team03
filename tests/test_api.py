"""Contract tests for the Lab 4 FastAPI application.

The API implementation is delivered by the other Lab 4 branches.  Until one of
the documented app modules exists, these tests are skipped so this testing-only
branch can remain reviewable and be rebased last, as required by the team plan.
"""

from __future__ import annotations

import importlib
import os
from collections.abc import AsyncIterator, Mapping
from typing import Any

import httpx
import pytest


APP_MODULE_CANDIDATES = (
    "assistant_api.main",
    "assistant_api.api",
    "api",
)


def _load_app() -> Any:
    configured_module = os.getenv("ASSISTANT_API_MODULE")
    candidates = (configured_module,) if configured_module else APP_MODULE_CANDIDATES
    missing_modules: list[str] = []

    for module_name in candidates:
        if not module_name:
            continue
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            root_package = module_name.split(".", maxsplit=1)[0]
            if exc.name not in {module_name, root_package}:
                raise
            missing_modules.append(module_name)
            continue

        app = getattr(module, "app", None)
        if app is None:
            pytest.fail(f"{module_name!r} exists but does not export `app`")
        return app

    pytest.skip(
        "Lab 4 API implementation has not been merged; tried: "
        + ", ".join(missing_modules)
    )


@pytest.fixture(scope="session")
def api_app() -> Any:
    return _load_app()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client(api_app: Any) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=api_app, raise_app_exceptions=False)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
        timeout=5.0,
    ) as async_client:
        yield async_client


def _resolve_schema(openapi: Mapping[str, Any], schema: Mapping[str, Any]) -> Mapping[str, Any]:
    reference = schema.get("$ref")
    if not reference:
        return schema

    resolved: Any = openapi
    for part in reference.removeprefix("#/").split("/"):
        resolved = resolved[part]
    return resolved


def _sample_value(name: str, schema: Mapping[str, Any]) -> Any:
    if "example" in schema:
        return schema["example"]
    if "default" in schema:
        return schema["default"]
    if schema.get("enum"):
        return schema["enum"][0]

    lowered = name.lower()
    named_samples = {
        "message": "Thư viện ở đâu?",
        "question": "Thư viện ở đâu?",
        "query": "Thư viện ở đâu?",
        "message_id": "test-message-001",
        "request_id": "test-request-001",
        "rating": 5,
        "score": 5,
        "helpful": True,
        "comment": "Câu trả lời hữu ích",
        "feedback": "Câu trả lời hữu ích",
    }
    if lowered in named_samples:
        return named_samples[lowered]

    value_type = schema.get("type", "string")
    return {
        "boolean": True,
        "integer": 1,
        "number": 1.0,
        "array": [],
        "object": {},
        "string": "test",
    }.get(value_type, "test")


def _request_example(api_app: Any, path: str, method: str) -> dict[str, Any]:
    openapi = api_app.openapi()
    operation = openapi["paths"][path][method]
    media_type = operation["requestBody"]["content"]["application/json"]
    schema = _resolve_schema(openapi, media_type["schema"])
    properties = schema.get("properties", {})
    required = schema.get("required", properties.keys())
    return {
        name: _sample_value(name, _resolve_schema(openapi, properties[name]))
        for name in required
    }


@pytest.mark.anyio
async def test_openapi_exposes_all_assigned_routes(api_app: Any) -> None:
    paths = api_app.openapi()["paths"]

    assert "get" in paths["/health"]
    assert "post" in paths["/v1/chat"]
    assert "post" in paths["/v1/feedback"]
    assert "get" in paths["/v1/weather"]


@pytest.mark.anyio
async def test_health_returns_ready_status(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert body.get("status", "ok").lower() in {"ok", "healthy", "ready"}


@pytest.mark.anyio
async def test_chat_returns_non_empty_answer(
    api_app: Any,
    client: httpx.AsyncClient,
) -> None:
    response = await client.post(
        "/v1/chat",
        json=_request_example(api_app, "/v1/chat", "post"),
    )

    assert response.status_code == 200
    body = response.json()
    answer = next(
        (body[key] for key in ("answer", "reply", "response", "message") if key in body),
        None,
    )
    assert isinstance(answer, str) and answer.strip()


@pytest.mark.anyio
async def test_chat_rejects_an_empty_body(client: httpx.AsyncClient) -> None:
    response = await client.post("/v1/chat", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_feedback_is_accepted(
    api_app: Any,
    client: httpx.AsyncClient,
) -> None:
    response = await client.post(
        "/v1/feedback",
        json=_request_example(api_app, "/v1/feedback", "post"),
    )

    assert response.status_code in {200, 201, 202}
    assert isinstance(response.json(), dict)


@pytest.mark.anyio
async def test_feedback_rejects_an_empty_body(client: httpx.AsyncClient) -> None:
    response = await client.post("/v1/feedback", json={})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_weather_validates_required_query_without_external_call(
    api_app: Any,
    client: httpx.AsyncClient,
) -> None:
    parameters = api_app.openapi()["paths"]["/v1/weather"]["get"].get(
        "parameters", []
    )
    required_query = [
        parameter
        for parameter in parameters
        if parameter.get("in") == "query" and parameter.get("required")
    ]
    if not required_query:
        pytest.skip("Weather endpoint does not define a required query parameter")

    response = await client.get("/v1/weather")

    assert response.status_code == 422
