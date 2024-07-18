import pytest
from unittest.mock import patch, Mock, MagicMock, create_autospec
from io import BytesIO
from observe_lambda_extension_telemetry_shipper.telemetry_subscriber import subscribe_to_telemetry_api, TelemetryHttpRequestHandler, handle_record
from observe_lambda_extension_telemetry_shipper.utils import TelemetryRecord, LogType
from observe_lambda_extension_telemetry_shipper.telemetry_subscriber import handle_record, TelemetryHandler
from datetime import datetime
import json

@pytest.fixture
def record():
    return TelemetryRecord(
        record_type=LogType.FUNCTION,
        record_time=datetime(2023, 1, 1, 12, 0),
        record='{"requestId": "1-2-3-4", "version": "$LATEST"}',
        raw={'time': '2023-01-01T12:00:00.000Z', 'type': 'function', 'record': {'requestId': '1-2-3-4', 'version': '$LATEST'}}
    )

@patch("observe_lambda_extension_telemetry_shipper.telemetry_subscriber.HTTPServer")
@patch("observe_lambda_extension_telemetry_shipper.telemetry_subscriber.lambda_service")
def test_subscribe_to_telemetry_api(mock_lambda_service, mock_http_server):
    subscribe_to_telemetry_api("test-id")
    mock_http_server.assert_called_once()
    mock_lambda_service.return_value.request.assert_called_once()

@patch("observe_lambda_extension_telemetry_shipper.telemetry_subscriber.handle_record")
def test_telemetry_http_request_handler(mock_handle_record):
    # Create a mock request with properly formatted JSON data
    mock_request = Mock()
    json_data = json.dumps([{"time": "2023-01-01T12:00:00.000Z", "type": "function", "record": {}}])
    mock_request.makefile.return_value = BytesIO(f"POST / HTTP/1.1\r\nContent-Length: {len(json_data)}\r\n\r\n{json_data}".encode())

    # Create a mock server and client address
    mock_server = Mock()
    client_address = ("127.0.0.1", 8080)

    # Create the handler with the mock request
    handler = TelemetryHttpRequestHandler(mock_request, client_address, mock_server)

    # Mock the necessary attributes and methods
    handler.rfile = BytesIO(json_data.encode())
    handler.headers = {"Content-Length": str(len(json_data))}
    handler.send_response = Mock()
    handler.end_headers = Mock()

    # Simulate the POST request
    handler.do_POST()

    # Assert that handle_record was called
    mock_handle_record.assert_called()

    # Additional assertions
    handler.send_response.assert_called_with(200)
    handler.end_headers.assert_called_once()

@patch.object(TelemetryHandler, '__subclasses__', return_value=[Mock()])
def test_handle_record(mock_subclasses, record):
    # Create a mock handler
    mock_handler = mock_subclasses.return_value[0]
    mock_handler.should_handle.return_value = True
    mock_handler.get_singleton.return_value = mock_handler

    # Call the function under test
    handle_record(record)

    # Assertions
    mock_handler.get_singleton.assert_called_once()
    mock_handler.should_handle.assert_called_once_with(record)
    mock_handler.handle.assert_called_once_with(record)
