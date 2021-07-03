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
            ModemSensor(
                "Compal Wifi Modem Model",
                compal_config,
                lambda modem: modem["model"],
            ),
            ModemSensor(
                "Compal Wifi Modem Hardware Version",
                compal_config,
                lambda modem: modem["hw_version"],
            ),
            ModemSensor(
                "Compal Wifi Modem Software Version",
                compal_config,
                lambda modem: modem["sw_version"].replace(modem["model"] + "-", "", 1),
            ),
            ModemSensor(
                "Compal Wifi Modem Operator",
                compal_config,
                lambda modem: modem["operator_id"],
            ),
            ModemSensor(
                "Compal Wifi Modem Uptime",
                compal_config,
                lambda modem: modem["uptime"].split(":", 1)[0],
            ),
        ]
    )


class ModemSensor(Entity):
    """Representation of a sensor."""

    def __init__(self, name, compal_config, attribute_accessor):
        """Initialize the sensor."""
        self._name = name
        self._compal_config = compal_config
        self._attribute_accessor = attribute_accessor
        self._state = attribute_accessor(compal_config.current_modem_state["modem"])

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

        self._state = self._attribute_accessor(
            self._compal_config.current_modem_state["modem"]
        )
