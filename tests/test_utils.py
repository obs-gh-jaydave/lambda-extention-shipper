import pytest
from observe_lambda_extension_telemetry_shipper.utils import never_fail, LogType, TelemetryRecord

def test_never_fail(caplog):
    with never_fail("test"):
        raise ValueError("Test exception")
    
    assert "An exception occurred in a never-fail code 'test'" in caplog.text
    assert "ValueError: Test exception" in caplog.text

@pytest.mark.parametrize(
    "record_type, expected",
    [
        ("platform.start", LogType.START),
        ("platform.end", LogType.END),
        ("platform.report", LogType.REPORT),
        ("function", LogType.FUNCTION),
        ("platform.runtimeDone", LogType.RUNTIME_DONE),
        ("platform.extension", LogType.OTHER),
    ],
)
def test_log_type_parse(record_type, expected):
    assert LogType.parse(record_type) == expected

def test_log_type_parse_unknown():
    with pytest.raises(ValueError):
        LogType.parse("unknown")

def test_telemetry_record_parse(raw_record):
    record = TelemetryRecord.parse(raw_record)
    assert record.record_type == LogType.FUNCTION
    assert record.record == '{"requestId": "1-2-3-4", "version": "$LATEST"}'
    assert record.record_time.isoformat() == "2023-01-01T12:00:00"