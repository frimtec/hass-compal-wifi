"""Platform for sensor integration."""
import threading
from datetime import datetime
from datetime import timedelta

from compal_wifi_switch import Commands

from homeassistant.helpers.entity import Entity
from . import DOMAIN


def modem_status(compal_config):
    def modem_status_blocking():
        compal_config.semaphore.acquire()
        try:
            compal_config.current_modem_state = Commands.status(
                compal_config.host, compal_config.password
            )
            compal_config.last_update = datetime.now()
        except:
            compal_config.last_update = compal_config.last_update - timedelta(
                seconds=compal_config.polling_interval
            )
        finally:
            compal_config.semaphore.release()

    compal_config.last_update = datetime.now()
    threading.Thread(
        target=modem_status_blocking,
    ).start()


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    compal_config = hass.data[DOMAIN]
    add_entities(
        [
            ModemSensor("Compal Wifi Modem Model", "model", compal_config),
            ModemSensor(
                "Compal Wifi Modem Hardware Version", "hw_version", compal_config
            ),
            ModemSensor(
                "Compal Wifi Modem Software Version", "sw_version", compal_config
            ),
            ModemSensor("Compal Wifi Modem Operator", "operator_id", compal_config),
            ModemSensor("Compal Wifi Modem Uptime", "uptime", compal_config),
        ]
    )


class ModemSensor(Entity):
    """Representation of a sensor."""

    def __init__(self, name, attribute, compal_config):
        """Initialize the sensor."""
        self._name = name
        self._attribute = attribute
        self._compal_config = compal_config
        self._state = compal_config.current_modem_state["modem"][attribute]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        if (datetime.now() - self._compal_config.last_update) > timedelta(
            seconds=self._compal_config.polling_interval
        ):
            modem_status(self._compal_config)

        self._state = self._compal_config.current_modem_state["modem"][self._attribute]
