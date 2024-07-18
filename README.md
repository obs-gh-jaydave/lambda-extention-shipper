# Observe Lambda Extension Telemetry Shipper

The Observe Lambda Extension Telemetry Shipper is a custom AWS Lambda extension that collects and ships telemetry data from Lambda functions directly to Observe. This extension allows you to monitor and analyze your Lambda function's performance and behavior without relying on CloudWatch Logs.

##Features
- Collects Lambda function telemetry data
- Ships data directly to Observe
- Configurable batch size and time for log shipping
- Supports Python 3.8 and 3.9 Lambda runtimes

## Installation
To use this extension with your Lambda function, you need to add it as a layer to your function. You can either use a pre-built layer or build it yourself.

Using a pre-built layer
Add the following ARN to your Lambda function's layers:
```
arn:aws:lambda:<region>:123456789012:layer:observe-lambda-extension-telemetry-shipper:1
```
Replace `<region>` with your AWS region and update the account ID and version number as necessary.

### Building the layer yourself
1. Clone this repository:
```
git clone https://github.com/observeinc/observe-lambda-extension-telemetry-shipper.git
cd observe-lambda-extension-telemetry-shipper
```
2. Build the extension:
```
./scripts/deploy.sh
```
3. The script will output the ARN for the newly created layer. Add this ARN to your Lambda function's layers.
## Configuration
Set the following environment variables in your Lambda function:

- `OBSERVE_ENDPOINT`: The Observe ingestion endpoint URL (required)
- `OBSERVE_API_KEY`: Your Observe API key (required)
- `OBSERVE_EXTENSION_LOG_BATCH_SIZE`: Maximum batch size in bytes before sending logs (default: 1000)
- `OBSERVE_EXTENSION_LOG_BATCH_TIME`: Maximum time in milliseconds before sending logs (default: 60000)
## Usage
Once the extension is added as a layer and configured, it will automatically start collecting and shipping telemetry data to Observe when your Lambda function is invoked.

## Local Testing with SAM CLI
You can test the extension locally using the AWS SAM CLI.

### Prerequisites
- AWS SAM CLI
### Setup
1. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate
    ```
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
### `template.yml`
The `template.yml` file is used by the SAM CLI to define the resources for your serverless application. It includes your Lambda function and the layer for the Observe Lambda Extension Telemetry Shipper.


```
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Resources:
  TestFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: test_lambda_function.lambda_handler
      Runtime: python3.10
      CodeUri: lambda-local-test/
      Layers:
        - !Ref ObserveLayer
      Environment:
        Variables:
          OBSERVE_ENDPOINT: "https://your-observe-endpoint.com"
          OBSERVE_API_KEY: "your-api-key"
  ObserveLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: observe_lambda_extension_telemetry_shipper
      ContentUri: ./dist/
      CompatibleRuntimes:
        - python3.10
```
### `lambda-local-test/test_lambda_function.py`

The `lambda-local-test/test_lambda_function.py` file contains a simple Lambda function used for local testing. This function uses the ObserveHandler to process telemetry data and send it to Observe.
```
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
```
5. Install the `requests` module and any other dependencies in the layer:
    ```
    mkdir -p dist/python
    pip install -r requirements.txt -t dist/python
    cp -r src/observe_lambda_extension_telemetry_shipper dist/python/
    ```
6. Build the project using SAM CLI:
    ```
    sam build
    ```
7. Invoke the function locally:
    ```
    sam local invoke TestFunction
    ```
## Deployment
To deploy the function to AWS using the provided ./scripts/deploy.sh script, follow these steps:

1. Ensure the script has execute permissions:
    ```
    chmod +x ./scripts/deploy.sh
    ```
2. Run the deployment script:
    ```
    ./scripts/deploy.sh
    ```
3. The script will output the ARN for the newly created layer. Add this ARN to your Lambda function's layers.
## Development
To set up the development environment:

1. Create a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate
    ```
2. Install development dependencies:

    ```
    pip install -e .[dev]
    ```
3. Run tests:
    ```
    pytest
    ```

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.