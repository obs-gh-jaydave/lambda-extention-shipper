#!/usr/bin/env bash
set -eo pipefail

# Run pre-commit hooks
pre-commit run -a

# Run pytest with coverage
python -m pytest --cov=src/observe_lambda_extension_telemetry_shipper tests/

# Run additional checks if needed (e.g., linting)
# flake8 src/observe_lambda_extension_telemetry_shipper tests/

echo "All checks passed successfully!"