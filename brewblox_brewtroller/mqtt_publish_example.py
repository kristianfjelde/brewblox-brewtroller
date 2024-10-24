"""
An example of how to publish MQTT events.

MQTT is a publish/subscribe message protocol.
In Brewblox it's commonly used to publish history data and service state.

For an explanation on MQTT, see https://randomnerdtutorials.com/what-is-mqtt-and-how-it-works/

For reference documentation on MQTT in Brewblox, see https://www.brewblox.com/dev/

The result is the same as https://www.brewblox.com/dev/tutorials/pubscript
but now as part of a service that can multiple things at the same time.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from random import random

from . import mqtt, utils

LOGGER = logging.getLogger(__name__)


async def run():
    config = utils.get_config()
    mqtt_client = mqtt.CV.get()

    history_topic: str = f'{config.mqtt_topic}/history/{config.name}'
    interval: float = config.publish_interval.total_seconds()
    value: float = 20

    state_topic: str = f'{config.mqtt_topic}/state/{config.name}'

    while True:
        await asyncio.sleep(interval)

        mqtt_client.publish(state_topic,
                            {
                                'key': config.name,
                                'type': 'Brewtroller.state.service',
                                'timestamp': utils.time_ms(),
                            })

        value += ((random() - 0.5) * 10)

        message = {
            'key': config.name,
            'type': 'Brewtroller.state',
            'data': {'value[degC]': value},
            'timestamp': utils.time_ms()
        }

        mqtt_client.publish(history_topic, message)
        LOGGER.info(f'sent {message}')


@asynccontextmanager
async def lifespan():
    # `utils.task_context()` wraps the async `run()` function
    # in a background task that starts now, and is cancelled when the context ends.
    async with utils.task_context(run()):
        yield
