import pytest
from observe_lambda_extension_telemetry_shipper.configuration import Configuration, parse_env, parse_env_to_bool, parse_env_to_int

def test_parse_env_exists(monkeypatch):
    monkeypatch.setenv("TEST_ENV", "value")
    assert parse_env("TEST_ENV", "default") == "value"

def test_parse_env_not_exists(monkeypatch):
    monkeypatch.delenv("TEST_ENV", raising=False)
    assert parse_env("TEST_ENV", "default") == "default"


@pytest.mark.parametrize(
    "actual_env, expected_result",
    [
        ("3", 3),
        ("0", 0),
        ("", 5),  # Test default value
        ("invalid", 5),  # Test invalid input
    ],
)
def test_parse_env_to_int(actual_env, expected_result, monkeypatch):
    monkeypatch.setenv("TEST_ENV", actual_env)
    assert parse_env_to_int("TEST_ENV", 5) == expected_result

@pytest.mark.parametrize(
    "actual_env, expected_result",
    [
        ("False", False),
        ("True", True),
        ("false", False),
        ("true", True),
        ("bad_value", False),
    ],
)
def test_parse_env_to_bool(actual_env, expected_result, monkeypatch):
    monkeypatch.setenv("TEST_ENV", actual_env)
    assert parse_env_to_bool("TEST_ENV", False) == expected_result

def test_configuration(monkeypatch):
    monkeypatch.setattr(Configuration, "observe_endpoint", "https://test.observe.com/ingest")
    monkeypatch.setattr(Configuration, "observe_api_key", "test-api-key")
    monkeypatch.setattr(Configuration, "function_name", "test-function")
    monkeypatch.setattr(Configuration, "min_batch_size", 2000)
    monkeypatch.setattr(Configuration, "min_batch_time", 30.0)

    assert Configuration.observe_endpoint == "https://test.observe.com/ingest"
    assert Configuration.observe_api_key == "test-api-key"
    assert Configuration.function_name == "test-function"
    assert Configuration.min_batch_size == 2000
    assert Configuration.min_batch_time == 30.0