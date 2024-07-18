#!/usr/bin/env bash
set -eo pipefail

# Configuration
LAYER_NAME="observe-lambda-extension-telemetry-shipper"
REGIONS=("us-west-2") # Add or remove regions as needed

# Build the extension
echo "Building the extension..."
rm -rf dist
python3 setup.py bdist_wheel

# Create a deployment package
echo "Creating deployment package..."
mkdir -p dist/extension
cp scripts/telemetry dist/extension/
unzip -q dist/*.whl -d dist/extension/
cd dist/extension && zip -r ../extension.zip . && cd ../..

# Deploy to specified regions
for region in "${REGIONS[@]}"; do
    echo "Deploying to region: $region"
    aws lambda publish-layer-version \
        --layer-name "$LAYER_NAME" \
        --description "Observe Lambda Extension Telemetry Shipper" \
        --license-info "Apache-2.0" \
        --zip-file fileb://dist/extension.zip \
        --compatible-runtimes python3.8 python3.9 \
        --region "$region"
done

echo "Deployment complete!"