import os
import json
import urllib.request

from observe_lambda_extension_telemetry_shipper.telemetry_handlers.logs_manager import LogsManager
from observe_lambda_extension_telemetry_shipper.telemetry_subscriber import subscribe_to_telemetry_api
from observe_lambda_extension_telemetry_shipper.utils import (
    get_logger,
    lambda_service,
    OBSERVE_EXTENSION_NAME,
    HEADERS_NAME_KEY,
    HEADERS_ID_KEY,
    never_fail,
)

EVENTS = ["INVOKE", "SHUTDOWN"]

def register_extension() -> str:
    body = json.dumps({"events": EVENTS})
    headers = {HEADERS_NAME_KEY: OBSERVE_EXTENSION_NAME}

    conn = lambda_service()
    conn.request("POST", "/2020-01-01/extension/register", body, headers=headers)
    extension_id = conn.getresponse().headers["Lambda-Extension-Identifier"]
    get_logger().debug(f"Extension registered with id {extension_id}")
    return extension_id

def extension_loop(extension_id):
    url = f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/event/next"
    ready_request = urllib.request.Request(url, headers={HEADERS_ID_KEY: extension_id})
    while True:
        event = json.loads(urllib.request.urlopen(ready_request).read())
        with never_fail("Send initial logs"):
            get_logger().debug(f"Extension got event {event}")
            LogsManager.get_singleton().send_batch_if_needed()
        if event.get("eventType") == "SHUTDOWN":
            with never_fail("send final batch"):
                LogsManager.get_singleton().send_batch()
            break

def main():
    extension_id = register_extension()
    subscribe_to_telemetry_api(extension_id)
    extension_loop(extension_id)

if __name__ == "__main__":
    main()