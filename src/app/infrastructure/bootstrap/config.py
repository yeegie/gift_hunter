from app.infrastructure.config import RootConfig
from typing import Dict
from yaml import safe_load


def load_yaml_file(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as stream:
            return safe_load(stream) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {file_path} not found.")
    except Exception as e:
        raise RuntimeError(f"Error loading YAML file {file_path}: {e}")


def get_config(
    telegram_config: str,
    database_config: str,
    webhook_config: str,
    payment_config: str,
) -> RootConfig:
    telegram_data = load_yaml_file(telegram_config).get('telegram', {})
    database_data = load_yaml_file(database_config).get('database', {})
    webhook_data = load_yaml_file(webhook_config).get('webhook', {})
    payment_data = load_yaml_file(payment_config).get('payment', {})

    config_data = {
        "telegram": telegram_data,
        "database": database_data,
        "webhook": webhook_data,
        "payment": payment_data,
    }

    return RootConfig(**config_data)
