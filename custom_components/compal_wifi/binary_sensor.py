"""Platform for binary_sensor integration."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from . import DOMAIN


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    compal_config = hass.data[DOMAIN]
    add_entities(
        [
            GuestWifiBinarySensor(compal_config),
            ModemConnectivityBinarySensor(compal_config),
            TelephoneLineBinarySensor(
                compal_config,
                0,
            ),
            TelephoneLineBinarySensor(
                compal_config,
                1,
            ),
        ]
    )


class GuestWifiBinarySensor(BinarySensorEntity):
    """representation of a Demo binary sensor."""

    def __init__(self, compal_config):
        """Initialize the demo sensor."""
        self._compal_config = compal_config

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return "Compal Wifi Modem Guest Wifi"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        guest_wifis = self._compal_config.current_modem_state["wifi_guest"]
        for quest_wifi in guest_wifis:
            if quest_wifi["enabled"]:
                return True
        return False

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        if self.is_on:
            return "mdi:wifi"
        return "mdi:wifi-off"


class ModemConnectivityBinarySensor(BinarySensorEntity):
    """representation of a Demo binary sensor."""

    def __init__(self, compal_config):
        """Initialize the demo sensor."""
        self._compal_config = compal_config

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return "Compal Wifi Modem Internet Connectivity"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._compal_config.current_modem_state["modem"]["status"] == "online"

    @property
    def device_class(self):
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {"state": self._compal_config.current_modem_state["modem"]["status"]}


class TelephoneLineBinarySensor(BinarySensorEntity):
    """Representation of a sensor."""

    def __init__(self, compal_config, line_index):
        """Initialize the sensor."""
        self._compal_config = compal_config
        self._line_index = line_index
        self._state = self.get_state()
        self._on_hook = self.get_on_hook()

    def get_state(self):
        return self._compal_config.current_modem_state["telephone_line"][
            self._line_index
        ]["mta_state"]

    def get_on_hook(self):
        return self._compal_config.current_modem_state["telephone_line"][
            self._line_index
        ]["on_hook"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return (
            "Compal Wifi Modem Telephone Line "
            + self._compal_config.current_modem_state["telephone_line"][
                self._line_index
            ]["line_number"]
        )

    @property
    def is_on(self):
        return self._state == "ready"

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.get_state()
        self._on_hook = self.get_on_hook()

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        return (
            "mdi:phone-off-outline"
            if self._state != "ready"
            else "mdi:phone-hangup" if self._on_hook else "mdi:phone-in-talk"
        )

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {
            "state": self._state,
            "on_hook": self._on_hook,
        }

    @property
    def device_class(self):
        return BinarySensorDeviceClass.CONNECTIVITY
