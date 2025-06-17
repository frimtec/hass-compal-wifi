import logging

_LOGGER = logging.getLogger(__name__)


class Commands:

    @staticmethod
    def status(host, password):
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
                {"radio": "2g", "enabled": True, "ssid": "WIFI-2G", "hidden": False},
                {"radio": "5g", "enabled": False, "ssid": "WIFI-5G", "hidden": False},
            ],
            "wifi_guest": [
                {
                    "radio": "2g",
                    "enabled": "on",
                    "mac": "**:**:**:**:**:**",
                    "ssid": "GUEST",
                    "hidden": False,
                },
                {
                    "radio": "5g",
                    "enabled": "off",
                    "mac": "",
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
        _LOGGER.info("WIFI band %s switched to %s", band, state)
        return

    @staticmethod
    def reboot(host, password):
        _LOGGER.info("Modem reset")
        return
