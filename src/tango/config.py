import tomllib
from pathlib import Path

from .logger import warning


def default_config() -> dict:
    return {
        "title": "Untitled Site",
        "deployment": {
            "base_path": "/",
        },
    }


def load_config(site_root: str) -> dict:
    config_path = Path(site_root) / "tango.toml"

    config = default_config()

    if not config_path.exists():
        warning("No tango.toml found, using defaults")
        return config

    with open(config_path, "rb") as file:
        user_config = tomllib.load(file)

    config.update(user_config)

    if "deployment" in user_config:
        config["deployment"].update(user_config["deployment"])

    return config
