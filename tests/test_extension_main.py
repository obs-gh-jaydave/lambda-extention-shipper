import pytest
from unittest.mock import Mock, patch
from observe_lambda_extension_telemetry_shipper.extension_main import register_extension, extension_loop, main

@pytest.fixture
def mock_lambda_service(monkeypatch):
    mock = Mock()
    mock.return_value.getresponse.return_value.headers = {"Lambda-Extension-Identifier": "test-id"}
    monkeypatch.setattr("observe_lambda_extension_telemetry_shipper.extension_main.lambda_service", mock)
    return mock

def test_register_extension(mock_lambda_service):
    result = register_extension()
    assert result == "test-id"
    mock_lambda_service.return_value.request.assert_called_once()

@patch("observe_lambda_extension_telemetry_shipper.extension_main.urllib.request.urlopen")
def test_extension_loop(mock_urlopen):
    mock_urlopen.return_value.read.side_effect = [
        b'{"eventType": "INVOKE"}',
        b'{"eventType": "SHUTDOWN"}'
    ]
    extension_loop("test-id")
    assert mock_urlopen.call_count == 2

@patch("observe_lambda_extension_telemetry_shipper.extension_main.register_extension")
@patch("observe_lambda_extension_telemetry_shipper.extension_main.subscribe_to_telemetry_api")
@patch("observe_lambda_extension_telemetry_shipper.extension_main.extension_loop")
def test_main(mock_extension_loop, mock_subscribe, mock_register):
    mock_register.return_value = "test-id"
    main()
    mock_register.assert_called_once()
    mock_subscribe.assert_called_once_with("test-id")
    mock_extension_loop.assert_called_once_with("test-id")