"""Support for WiFi switches using Compal modem."""
import threading
from datetime import datetime

from homeassistant.helpers.entity import ToggleEntity

from compal_wifi_switch import Switch, Band, Commands

from .const import (
    DOMAIN,
)


def extract_wifi_state(status):
    states = {}
    for wifi_band in status["wifi"]:
        states[wifi_band["radio"]] = wifi_band["enabled"]
    return states


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Compal WiFi devices."""
    if discovery_info is None:
        return

    compal_config = hass.data[DOMAIN]
    states = extract_wifi_state(compal_config.current_modem_state)

    switches = [
        CompalWifiSwitch(compal_config, Band.BAND_2G, states[Band.BAND_2G.value]),
        CompalWifiSwitch(compal_config, Band.BAND_5G, states[Band.BAND_5G.value]),
    ]
    all_switches = [CompalCompositWifiSwitch(compal_config, switches)]
    all_switches.extend(switches)
    add_entities(all_switches, True)

    return True


class CompalConfig:
    def __init__(self, host, password, pause, guest):
        self.host = host
        self.password = password
        self.pause = pause
        self.guest = guest
        self.semaphore = threading.Semaphore()


class WifiSwitch:
    def set_processing_state(self, state: str):
        pass

    def config(self) -> CompalConfig:
        pass

    def internal_state(self) -> bool:
        pass


def switch_wifi(wifi_switch: WifiSwitch, state, band):
    compal_config = wifi_switch.config()
    wifi_switch.set_processing_state("on")

    def switch_wifi_blocking():
        compal_config.semaphore.acquire()
        enable_guest = False
        if state == Switch.ON:
            enable_guest = compal_config.guest
        new_processing_state = None
        try:
            Commands.switch(
                compal_config.host,
                compal_config.password,
                state,
                band,
                enable_guest,
                compal_config.pause,
            )
            new_processing_state = "off"
        except:
            new_processing_state = "error"
        finally:
            try:
                compal_config.current_modem_state = Commands.status(
                    compal_config.host, compal_config.password
                )
                compal_config.last_update = datetime.now()
                compal_config.update_state = "ok"
            except:
                compal_config.update_state = "error"
            finally:
                wifi_switch.set_processing_state(new_processing_state)
                compal_config.semaphore.release()

    threading.Thread(
        target=switch_wifi_blocking,
    ).start()


class CompalWifiSwitch(ToggleEntity, WifiSwitch):
    """Represent a Compal WiFi."""

    def __init__(self, config, radio, initial_state):
        self._config = config
        self._radio = radio
        self._name = f"wifi.{radio}"
        self._state = initial_state
        self._switch_progress = "off"

    def set_processing_state(self, state):
        self._switch_progress = state

    def config(self) -> CompalConfig:
        return self._config

    def internal_state(self) -> bool:
        return self._state

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the entity."""
        if self._switch_progress != "on":
            self._state = extract_wifi_state(self._config.current_modem_state)[
                self._radio.value
            ]
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        switch_wifi(self, Switch.ON, self._radio)
        self._state = True

    def turn_off(self, **kwargs):
        """Turn the device off."""
        switch_wifi(self, Switch.OFF, self._radio)
        self._state = False

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {"switch_progress": self._switch_progress}

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        if self.is_on:
            return "mdi:wifi"
        return "mdi:wifi-off"


class CompalCompositWifiSwitch(ToggleEntity, WifiSwitch):
    """Represent a Compal WiFi."""

    def __init__(self, config, switches):
        self._config = config
        self._switches = switches
        self._name = f"wifi.{Band.ALL}"
        self._switch_progress = "off"

    def set_processing_state(self, state):
        self._switch_progress = state
        for switch in self._switches:
            switch.set_processing_state(state)

    def config(self) -> CompalConfig:
        return self._config

    def internal_state(self) -> bool:
        for switch in self._switches:
            if not switch.internal_state():
                return False
        return True

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the entity."""
        return self.internal_state()

    def turn_on(self, **kwargs):
        """Turn the device on."""
        for switch in self._switches:
            switch._state = True
        switch_wifi(self, Switch.ON, Band.ALL)

    def turn_off(self, **kwargs):
        """Turn the device off."""
        for switch in self._switches:
            switch._state = False
        switch_wifi(self, Switch.OFF, Band.ALL)

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {"switch_progress": self._switch_progress}

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        if self.internal_state():
            return "mdi:wifi"
        return "mdi:wifi-off"
