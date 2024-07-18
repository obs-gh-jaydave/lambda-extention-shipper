import sys
import os
sys.path.append("/opt")

import logging
import json
from datetime import datetime
from observe_lambda_extension_telemetry_shipper import ObserveHandler
from observe_lambda_extension_telemetry_shipper.utils import TelemetryRecord, LogType
from observe_lambda_extension_telemetry_shipper.configuration import Configuration

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Set configuration values
Configuration.observe_endpoint = os.getenv('OBSERVE_ENDPOINT')
Configuration.observe_api_key = os.getenv('OBSERVE_API_KEY')
Configuration.function_name = os.getenv('AWS_LAMBDA_FUNCTION_NAME')

def lambda_handler(event, context):
    logger.info("Lambda handler started")
    try:
        handler = ObserveHandler()
        
        telemetry_data = [
            TelemetryRecord(
                record_type=LogType.FUNCTION,
                record_time=datetime.strptime("2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"),
                record=json.dumps({"message": "Wade is cool."}),
                raw={
                    "timestamp": "2023-01-01T12:00:00",
                    "type": "FUNCTION",
                    "record": {"message": "Wade is cool."}
                }
            )
        ]
        
        result = handler.handle_logs(telemetry_data)
        logger.info(f'Logs sent to Observe: {result}')
        return {
            "statusCode": 200,
            "body": json.dumps(f'Logs sent to Observe: {result}')
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }


def lambda_handler_simple(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }