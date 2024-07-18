import json
import requests
from typing import List
from datetime import datetime  # Add this line

from observe_lambda_extension_telemetry_shipper.configuration import Configuration
from observe_lambda_extension_telemetry_shipper.export_logs_handlers.base_handler import ExportLogsHandler
from observe_lambda_extension_telemetry_shipper.utils import get_logger, TelemetryRecord

class ObserveHandler(ExportLogsHandler):
    def handle_logs(self, records: List[TelemetryRecord]) -> bool:
        if Configuration.observe_endpoint and records:
            get_logger().debug("ObserveHandler started to run")
            formatted_records = self.format_records(records)
            response = self.send_to_observe(formatted_records)
            if response.status_code == 200:
                get_logger().info(f"ObserveHandler sent {len(records)} logs to Observe")
                return True
            else:
                get_logger().error(f"Failed to send logs to Observe. Status code: {response.status_code}")
        return False

    @staticmethod
    def format_records(records: List[TelemetryRecord]) -> List[dict]:
        return [
            {
                "timestamp": r.record_time.isoformat() if isinstance(r.record_time, datetime) else r.record_time,
                "type": r.record_type.value,
                "content": json.loads(r.record),
                "aws_request_id": json.loads(r.record).get("aws_request_id", ""),
                "function_name": Configuration.function_name,
            } for r in records
        ]

    @staticmethod
    def send_to_observe(formatted_records: List[dict]) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Configuration.observe_api_key}"
        }
        data = json.dumps(formatted_records)
        return requests.post(Configuration.observe_endpoint, headers=headers, data=data)