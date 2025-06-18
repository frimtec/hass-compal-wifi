import logging
import time

from compal_wifi_switch import Switch, Band

_LOGGER = logging.getLogger(__name__)


class Commands:

    band_states = {
        Band.BAND_2G: True,
        Band.BAND_5G: False,
        Band.ALL: False,
    }

    @staticmethod
    def status(host, password):
        _LOGGER.info("Read status")
        time.sleep(1)
        return {
            "modem": {
                "model": "CH7465LG",
                "hw_version": "5.01",
                "sw_version": "CH7465LG-NCIP-6.15.31p1-NOSH",
                "cm_serial_number": "************",
                "cm_mac_addr": "**:**:**:**:**:**",
                "operator_id": "LIBERTYGLOBAL",
                "network_mode": "IPv4",
                "status": "unknown",
                "uptime": "50day(s)0h:12m:28s",
            },
            "wifi": [
                {
                    "radio": "2g",
                    "enabled": Commands.band_states[Band.BAND_2G],
                    "ssid": "WIFI-2G",
                    "hidden": False,
                },
                {
                    "radio": "5g",
                    "enabled": Commands.band_states[Band.BAND_5G],
                    "ssid": "WIFI-5G",
                    "hidden": False,
                },
            ],
            "wifi_guest": [
                {
                    "radio": "2g",
                    "enabled": Commands.band_states[Band.BAND_2G],
                    "mac": "**:**:**:**:**:**",
                    "ssid": "GUEST",
                    "hidden": False,
                },
                {
                    "radio": "5g",
                    "enabled": Commands.band_states[Band.BAND_5G],
                    "mac": "**:**:**:**:**:**",
                    "ssid": "GUEST",
                    "hidden": False,
                },
            ],
            "telephone_line": [
                {
                    "line_number": "1",
                    "provisioning_state": "on",
                    "on_hook": "on_hook",
                    "mta_state": "",
                },
                {
                    "line_number": "2",
                    "provisioning_state": "off",
                    "on_hook": "on_hook",
                    "mta_state": "",
                },
            ],
        }

    @staticmethod
    def switch(host, password, state, band, guest, pause, verbose=False):
        _LOGGER.info("Switch WIFI band %s to %s (guest=%d)", band, state, guest)
        time.sleep(pause)
        if band == Band.ALL:
            Commands.band_states[Band.BAND_2G] = state
            Commands.band_states[Band.BAND_5G] = state
        else:
            Commands.band_states[Band.band] = state

    @staticmethod
    def reboot(host, password):
        _LOGGER.info("Modem rebooted")
        time.sleep(20)
