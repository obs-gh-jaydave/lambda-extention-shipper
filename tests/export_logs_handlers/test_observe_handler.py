import pytest
from unittest.mock import Mock, patch
from observe_lambda_extension_telemetry_shipper.export_logs_handlers.observe_handler import ObserveHandler
from observe_lambda_extension_telemetry_shipper.utils import TelemetryRecord, LogType
from observe_lambda_extension_telemetry_shipper.configuration import Configuration
from datetime import datetime, timezone

@pytest.fixture
def sample_records():
    return [
        TelemetryRecord(LogType.START, datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc), '{"aws_request_id":"123"}', {}),
        TelemetryRecord(LogType.FUNCTION, datetime(2023, 1, 1, 0, 0, 1, tzinfo=timezone.utc), '{"aws_request_id":"123","message":"test"}', {}),
        TelemetryRecord(LogType.END, datetime(2023, 1, 1, 0, 0, 2, tzinfo=timezone.utc), '{"aws_request_id":"123"}', {}),
    ]

def test_format_records(sample_records):
    formatted = ObserveHandler.format_records(sample_records)
    assert len(formatted) == 3
    assert formatted[0]["type"] == "START"
    assert formatted[1]["type"] == "FUNCTION"
    assert formatted[2]["type"] == "END"
    assert all(record["function_name"] == Configuration.function_name for record in formatted)
    assert all(record["aws_request_id"] == "123" for record in formatted)

@patch('requests.post')
def test_send_to_observe(mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    formatted_records = [{"test": "data"}]
    response = ObserveHandler.send_to_observe(formatted_records)

    assert response.status_code == 200
    mock_post.assert_called_once_with(
        Configuration.observe_endpoint,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Configuration.observe_api_key}"
        },
        data='[{"test": "data"}]'
    )

@patch('requests.post')
def test_handle_logs_success(mock_post, sample_records):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    handler = ObserveHandler()
    result = handler.handle_logs(sample_records)

    assert result is True
    mock_post.assert_called_once()

@patch('requests.post')
def test_handle_logs_failure(mock_post, sample_records):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    handler = ObserveHandler()
    result = handler.handle_logs(sample_records)

    assert result is False
    mock_post.assert_called_once()

def test_handle_logs_no_config(sample_records):
    with patch('observe_lambda_extension_telemetry_shipper.configuration.Configuration') as mock_config:
        mock_config.observe_endpoint = None
        handler = ObserveHandler()
        result = handler.handle_logs(sample_records)

    assert result is False