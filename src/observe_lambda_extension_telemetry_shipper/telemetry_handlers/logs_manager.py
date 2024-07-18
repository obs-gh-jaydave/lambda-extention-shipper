from datetime import datetime
from typing import List

from observe_lambda_extension_telemetry_shipper.configuration import Configuration
from observe_lambda_extension_telemetry_shipper.export_logs_handlers.observe_handler import ObserveHandler
from observe_lambda_extension_telemetry_shipper.telemetry_handlers.base_handler import TelemetryHandler
from observe_lambda_extension_telemetry_shipper.utils import get_logger, TelemetryRecord, LogType

class LogsManager(TelemetryHandler):
    def __init__(self):
        self.last_sent_time: datetime = datetime.now()
        self.pending_logs: List[TelemetryRecord] = []
        self.pending_logs_size: int = 0

    def should_handle(self, record: TelemetryRecord) -> bool:
        return record.record_type == LogType.FUNCTION

    def handle(self, record: TelemetryRecord) -> None:
        self.pending_logs.append(record)
        self.pending_logs_size += len(record.record)

    def send_batch_if_needed(self) -> bool:
        big_batch = self.pending_logs_size >= Configuration.min_batch_size
        old_batch = (
            datetime.now() - self.last_sent_time
        ).total_seconds() >= Configuration.min_batch_time
        if big_batch or old_batch:
            self.send_batch()
            return True
        return False

    def send_batch(self) -> bool:
        self.last_sent_time = datetime.now()
        if not self.pending_logs:
            return False
        sorted_logs = sorted(self.pending_logs, key=lambda r: r.record_time)
        self.pending_logs.clear()
        self.pending_logs_size = 0
        
        try:
            ObserveHandler().handle_logs(sorted_logs)
        except Exception:
            get_logger().exception("Exception while handling ObserveHandler", exc_info=True)
        else:
            get_logger().debug("ObserveHandler finished successfully")
        return True