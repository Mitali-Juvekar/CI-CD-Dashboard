import yaml
import os

def parse_config(repo_path, config_file='.build-config.yml'):
    """Parse CI/CD configuration file from repository"""
    config_path = os.path.join(repo_path, config_file)
    
    # Default configuration if file doesn't exist
    default_config = {
        'build': {
            'image': 'python:3.9',
            'steps': [
                'pip install -r requirements.txt',
                'python -m pytest'
            ]
        },
        'test': {
            'unit': {
                'command': 'python -m pytest tests/unit',
                'timeout': 300
            },
            'integration': {
                'command': 'python -m pytest tests/integration',
                'timeout': 600
            }
        },
        'cache': {
            'paths': ['~/.cache/pip']
        }
    }
    
    if not os.path.exists(config_path):
        return default_config
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error parsing config file: {e}")
        return default_config