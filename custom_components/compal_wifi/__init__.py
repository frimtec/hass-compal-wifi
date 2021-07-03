"""The Compal WiFi component."""
import threading
from datetime import datetime
from datetime import timedelta

from compal_wifi_switch import Commands

from homeassistant.const import CONF_HOST, CONF_PASSWORD

DOMAIN = "compal_wifi"

CONF_PAUSE = "pause"
DEFAULT_PAUSE = 60

CONF_GUEST = "guest"
DEFAULT_GUEST = False

CONF_POLLING_INTERVAL = "polling_interval"
DEFAULT_POLLING_INTERVAL = 60 * 60

ATTR_RADIO = "radio"
DEFAULT_RADIO = "all"


def modem_reboot(compal_config):
    def modem_reboot_blocking():
        compal_config.semaphore.acquire()
        try:
            Commands.reboot(compal_config.host, compal_config.password)
            return True
        except:
            return False
        finally:
            compal_config.last_update = compal_config.last_update - timedelta(
                seconds=compal_config.polling_interval
            )
            compal_config.semaphore.release()

    threading.Thread(
        target=modem_reboot_blocking,
    ).start()


def setup(hass, config):
    """Your controller/hub specific code."""

    domain_config = config[DOMAIN]
    states = Commands.status(domain_config[CONF_HOST], domain_config[CONF_PASSWORD])

    compal_config = CompalConfig(
        domain_config[CONF_HOST],
        domain_config[CONF_PASSWORD],
        domain_config.get(CONF_PAUSE, DEFAULT_PAUSE),
        domain_config.get(CONF_GUEST, DEFAULT_GUEST),
        domain_config.get(CONF_POLLING_INTERVAL, DEFAULT_POLLING_INTERVAL),
        states,
    )

    # Data that you want to share with your platforms
    hass.data[DOMAIN] = compal_config

    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)
    hass.helpers.discovery.load_platform("switch", DOMAIN, {}, config)

    def handle_reboot(call):
        modem_reboot(compal_config)

    hass.services.register(DOMAIN, "reboot", handle_reboot)
    return True


class CompalConfig:
    def __init__(
        self, host, password, pause, guest, polling_interval, current_modem_state
    ):
        self.host = host
        self.password = password
        self.pause = pause
        self.guest = guest
        self.polling_interval = polling_interval
        self.current_modem_state = current_modem_state
        self.last_update = datetime.now()
        self.semaphore = threading.Semaphore()
