"""Configuration loader: reads API key and settings from Data/API.env or environment variables.

Supports both simple key format and KEY=VALUE pairs in API.env file.
Environment variables take precedence over file values.
"""
import os
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from Data/API.env and environment variables.
    
    Returns:
        Dict with keys: SERPAPI_KEY, OUTPUT_DIR, MIN_CITATIONS, 
                       API_RATE_LIMIT, MAX_RETRIES, REQUEST_TIMEOUT
    """
    data_dir = Path.cwd() / "Data"
    api_file = data_dir / "API.env"
    cfg: Dict[str, Any] = {}

    # Read from API.env file if it exists
    if api_file.exists():
        try:
            text = api_file.read_text(encoding='utf-8').strip()
            for line in text.splitlines():
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                    
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip()
                    # Remove quotes if present
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]
                    if v.startswith("'") and v.endswith("'"):
                        v = v[1:-1]
                    cfg[k] = v
        except Exception as e:
            import logging
            logging.warning(f"Error reading API.env: {e}")

    # Environment variables override file values
    cfg['SERPAPI_KEY'] = os.getenv('SERPAPI_KEY', cfg.get('SERPAPI_KEY', ''))
    cfg['OUTPUT_DIR'] = os.getenv('OUTPUT_DIR', cfg.get('OUTPUT_DIR', str(data_dir)))
    cfg['MIN_CITATIONS'] = int(os.getenv('MIN_CITATIONS', cfg.get('MIN_CITATIONS', '0')))
    cfg['API_RATE_LIMIT'] = float(os.getenv('API_RATE_LIMIT', cfg.get('API_RATE_LIMIT', '1')))
    cfg['MAX_RETRIES'] = int(os.getenv('MAX_RETRIES', cfg.get('MAX_RETRIES', '3')))
    cfg['REQUEST_TIMEOUT'] = int(os.getenv('REQUEST_TIMEOUT', cfg.get('REQUEST_TIMEOUT', '30')))
    
    # Validate critical config
    if not cfg['SERPAPI_KEY'] or cfg['SERPAPI_KEY'] == 'your_serpapi_key_here':
        raise ValueError(
            "SERPAPI_KEY not configured. Please set it in Data/API.env or SERPAPI_KEY environment variable"
        )
    
    return cfg
