"""
Pydantic models are declared here, and then imported wherever needed
"""

from datetime import timedelta
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceConfig(BaseSettings):
    """
    Global service configuration.

    Pydantic Settings (https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
    provides the `BaseSettings` model that loads values from environment variables.

    To access the loaded model, we use `utils.get_config()`.
    """
    model_config = SettingsConfigDict(
        # `name` is now loaded from the environment variable `brewblox_brewtroller_name`
        env_prefix='brewblox_brewtroller_',

        # You can use either `brewblox_brewtroller_name=name` or `YOUR_PACKAGE_NAME=name`
        case_sensitive=False,

        # Ignores all unknown environment variables that happen to have the same prefix
        json_schema_extra='ignore',
    )

    name: str = 'brewtroller'
    debug: bool = False

    mqtt_protocol: Literal['mqtt', 'mqtts'] = 'mqtt'
    mqtt_host: str = 'eventbus'
    mqtt_port: int = 1883

    mqtt_topic: str = 'brewcast'
    publish_interval: timedelta = timedelta(seconds=5)

    bt_url: str = 'http://brewtroller'
    simulation: bool = False


class ExampleMessage(BaseModel):
    """
    The data model for the example HTTP endpoint.

    For more options, see https://docs.pydantic.dev/latest/
    """
    content: str
