import typing
from dataclasses import dataclass
from pathlib import Path

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class Config:
    username: str
    password: str


def setup_config(app: 'Application'):
    raw_config = Path('config/config.yaml').read_text()
    config = yaml.safe_load(raw_config)
    app.config = Config(
        username=config['credentials']['username'],
        password=config['credentials']['password']
    )