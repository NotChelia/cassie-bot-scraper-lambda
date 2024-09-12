import logging.config
import pathlib

import yaml


def setup_logging():
    """Setup logging from YAML cofig"""
    config_file = pathlib.Path("logconfig.yaml")
    with open(config_file) as f_in:
        config = yaml.safe_load(f_in)

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    return logger
