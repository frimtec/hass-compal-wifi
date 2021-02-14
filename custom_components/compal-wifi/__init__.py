import threading
import logging
import sys

from compal_wifi_switch import (Switch, Band, Commands)

from homeassistant.const import CONF_HOST, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

DOMAIN = "compal_wifi"

CONF_PAUSE = "pause"
DEFAULT_PAUSE = 60

CONF_GUEST_MACS_2G = "guest_macs_2g"
DEFAULT_GUEST_MACS_2G = []

CONF_GUEST_MACS_5G = "guest_macs_5g"
DEFAULT_GUEST_MACS_5G = []

ATTR_RADIO = "radio"
DEFAULT_RADIO = "all"


def setup(hass, config):

    host = config[DOMAIN][CONF_HOST]
    password = config[DOMAIN][CONF_PASSWORD]
    pause = config[DOMAIN].get(CONF_PAUSE, DEFAULT_PAUSE)
    guest_macs_2g = config[DOMAIN].get(CONF_GUEST_MACS_2G, DEFAULT_GUEST_MACS_2G)
    guest_macs_5g = config[DOMAIN].get(CONF_GUEST_MACS_5G, DEFAULT_GUEST_MACS_5G)
    pause = config[DOMAIN].get(CONF_PAUSE, DEFAULT_PAUSE)
    semaphore = threading.Semaphore()

    def set_radio_state(_band, state_value):
        if _band == Band.ALL:
            bands = [Band.BAND_2G, Band.BAND_5G]
        else:
            bands = [_band]
        for real_band in bands:
            hass.states.set(f"compal_wifi.{real_band}", state_value)

    def switch_wifi_blocking(_host, _password, _state, _band, _guest, _pause):
        semaphore.acquire()
        try:
            set_radio_state(_band, "changing")
            Commands.switch(_host, _password, _state, _band, _guest, _pause)
            set_radio_state(_band, f"{_state}")
        except:
            _LOGGER.error("Unexpected error:", sys.exc_info()[0])
            set_radio_state(_band, "error")
        finally:
            semaphore.release()

    def switch_wifi(state, band, guest):
        threading.Thread(target=switch_wifi_blocking, args=(host, password, state, band, guest, pause)).start()

    def handle_wifi_on(call):
        radio = Band(call.data.get(ATTR_RADIO, DEFAULT_RADIO))
        all_guest_macs = []
        if radio == Band.ALL or radio == Band.BAND_2G:
            all_guest_macs.extend(guest_macs_2g)
        if radio == Band.ALL or radio == Band.BAND_5G:
            all_guest_macs.extend(guest_macs_5g)

        switch_wifi(Switch.ON, radio, all_guest_macs)

    def handle_wifi_off(call):
        radio = Band(call.data.get(ATTR_RADIO, DEFAULT_RADIO))
        switch_wifi(Switch.OFF, radio, [])

    hass.services.register(DOMAIN, "wifi_on", handle_wifi_on)
    hass.services.register(DOMAIN, "wifi_off", handle_wifi_off)

    status = Commands.status(host, password)
    for wifi_band in status['wifi']:
        set_radio_state(wifi_band['radio'], 'on' if wifi_band['enabled'] else 'off')

    return True
