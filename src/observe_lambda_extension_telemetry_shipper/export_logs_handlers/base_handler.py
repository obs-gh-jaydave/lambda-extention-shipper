from abc import ABC, abstractmethod
from typing import List

from observe_lambda_extension_telemetry_shipper.utils import TelemetryRecord

class ExportLogsHandler(ABC):
    @abstractmethod
    def handle_logs(self, records: List[TelemetryRecord]):
        raise NotImplementedError()