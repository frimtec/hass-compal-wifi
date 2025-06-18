"""The Compal WiFi component."""

import logging
import threading
from datetime import datetime

from compal_wifi_switch import Commands as RealModem
from .modem_simulator import Commands as VirtualModem

from homeassistant.helpers.discovery import load_platform
from homeassistant.const import CONF_HOST, CONF_PASSWORD


from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONF_PAUSE = "pause"
DEFAULT_PAUSE = 70

CONF_GUEST = "guest"
DEFAULT_GUEST = False

CONF_POLLING_INTERVAL = "polling_interval"
DEFAULT_POLLING_INTERVAL = 15 * 60

ATTR_RADIO = "radio"
DEFAULT_RADIO = "all"


def modem_status(compal_config):
    def modem_status_blocking():
        compal_config.semaphore.acquire()
        try:
            compal_config.current_modem_state = compal_config.modem.status(
                compal_config.host, compal_config.password
            )
            compal_config.last_update = datetime.now()
            compal_config.update_state = "ok"
        except:
            compal_config.update_state = "error"
        finally:
            compal_config.semaphore.release()

    threading.Thread(
        target=modem_status_blocking,
    ).start()


def modem_reboot(compal_config):
    def modem_reboot_blocking():
        compal_config.semaphore.acquire()
        try:
            compal_config.modem.reboot(compal_config.host, compal_config.password)
            return True
        except:
            return False
        finally:
            compal_config.semaphore.release()

    threading.Thread(
        target=modem_reboot_blocking,
    ).start()


def setup(hass, config):
    """Your controller/hub specific code."""

    domain_config = config[DOMAIN]

    host = domain_config[CONF_HOST]
    password = domain_config[CONF_PASSWORD]
    modem = RealModem
    if host == "0.0.0.0":
        modem = VirtualModem
        _LOGGER.warning("Using virtual modem for testing")

    states = modem.status(host, password)

    compal_config = CompalConfig(
        host,
        password,
        domain_config.get(CONF_PAUSE, DEFAULT_PAUSE),
        domain_config.get(CONF_GUEST, DEFAULT_GUEST),
        domain_config.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL),
        states,
        modem,
    )

    # Data that you want to share with your platforms
    hass.data[DOMAIN] = compal_config

    load_platform(hass, "sensor", DOMAIN, {}, config)
    load_platform(hass, "binary_sensor", DOMAIN, {}, config)
    load_platform(hass, "switch", DOMAIN, {}, config)

    def handle_reboot(call):
        modem_reboot(compal_config)

    def handle_poll_now(call):
        modem_status(compal_config)

    hass.services.register(DOMAIN, "reboot", handle_reboot)
    hass.services.register(DOMAIN, "poll_now", handle_poll_now)
    return True


class CompalConfig:
    def __init__(
        self, host, password, pause, guest, polling_interval, current_modem_state, modem
    ):
        self.host = host
        self.password = password
        self.pause = pause
        self.guest = guest
        self.polling_interval = polling_interval
        self.current_modem_state = current_modem_state
        self.last_update = datetime.now()
        self.update_state = "ok"
        self.semaphore = threading.Semaphore()
        self.modem = modem
