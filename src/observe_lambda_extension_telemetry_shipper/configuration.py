import os
from typing import Optional

def parse_env(env_name: str, default: Optional[str] = None) -> Optional[str]:
    try:
        return os.environ.get(env_name, default)
    except KeyError:
        return default
    

def parse_env_to_bool(env_name: str, default: bool) -> bool:
    try:
        return parse_env(env_name, str(default)).lower() == "true"
    except ValueError:
        return default
    

def parse_env_to_int(env_name: str, default: int) -> int:
    try:
        return int(parse_env(env_name, str(default)))
    except ValueError:
        return default

class Configuration:
    observe_endpoint: str = parse_env("OBSERVE_ENDPOINT", "https://api.observeinc.com/v1/ingest")
    observe_api_key: str = parse_env("OBSERVE_API_KEY")
    function_name: str = parse_env("AWS_LAMBDA_FUNCTION_NAME", "Unknown")
    min_batch_size: int = parse_env_to_int("OBSERVE_EXTENSION_LOG_BATCH_SIZE", 1_000)
    min_batch_time: float = parse_env_to_int("OBSERVE_EXTENSION_LOG_BATCH_TIME", 60_000) / 1_000