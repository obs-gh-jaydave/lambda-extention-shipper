import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="observe_lambda_extension_telemetry_shipper",
    version="0.1.0",
    author="Observe Inc.",
    author_email="support@observeinc.com",
    description="A Lambda extension to ship telemetry data to Observe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/observeinc/observe-lambda-extension-telemetry-shipper",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.1,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5,<7.0.0",
            "pytest-cov>=2.12.1,<3.0.0",
            "flake8>=3.9.2,<4.0.0",
            "black>=21.7b0,<22.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "observe-lambda-extension=observe_lambda_extension_telemetry_shipper.extension_main:main",
        ],
    },
)