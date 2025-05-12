# Compal Wi-Fi integration for Home Assistant
[![hacs_badge][hacs-shield]][hacs]
![Project Maintenance][maintenance-shield]
[![License][license-shield]][license]

![Downloads][downloads-shield]
![Downloads][downloads-latest-shield]


[![Build Status][build-status-shield]][build-status]
[![Deploy Status][deploy-status-shield]][deploy-status]

![Icon](images/icon-readme.png)

---
**_Contributions Only:_**
_I no longer have a Compal modem and can therefore not actively work on this project anymore.
So all future development will be from pull requests submitted by the community.  
What I will do:_
* _review pull requests_
* _publish new releases upon request_
---

Home Assistant component to switch Wi-Fi of the modem Compal CH7465LG on or off.
The component is tested with the following modem firmware versions:
* ```NCIP-6.15.30-1p3-1-NOSH```
* ```NCIP-6.15.30-1p6-NOSH```
*  ```NCIP-6.15.31p1-NOSH```

![WiFi switches!](images/compal-wifi.png)

This component is not official, developed, supported or endorsed by Compal.

## Installation

1. Using the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory there, you need to create it.
3. Create an empty directory `compal_wifi` inside the directory `custom_components`.
4. Download the ZIP archive `compal_wifi.zip` from the [latest release assets][latest-release].   
5. Extract the downloaded ZIP archive to the directory `custom_components/compal_wifi`.
6. Move on to the configuration in the file `configuration.yaml`.
7. Restart Home Assistant.

## Configuration 
 
Add a configuration to your `configuration.yaml` file:
``` yaml
compal_wifi:
    host: 192.168.1.1
    password: YOUR_PASSWORD
```

### Configuration options

| Key                | Type     | Required | Description                                                         |
|--------------------|----------|----------|---------------------------------------------------------------------|
| `host`             | `string` | `True`   | The hostname or IP address of your compal modem, e.g., 192.168.0.1. |
| `password`         | `string` | `True`   | The password for your modems administration account.                |
| `guest`            | `bool`   | `False`  | Enable guest network when switching ON WIFI.                        |
| `pause`            | `int`    | `False`  | Number of seconds to wait between modem changes (default 70s).      |
| `polling_interval` | `int`    | `False`  | Number of seconds to poll modem state (default 900s - 15m).         |

## Platforms

### Switch
The component offers three switches to turn Wi-Fi bands on or off:

| Entity            | Description                   |
|-------------------|-------------------------------|
| `switch.wifi_2g`  | Switch for 2.4 GHz WiFi band. |
| `switch.wifi_5g`  | Switch for 5 GHz WiFi band.   |
| `switch.wifi_all` | Switch for both WiFi bands.   |

Be aware, switching Wi-Fi bands on or off are slow operations. If you want to switch all bands on or off better use the
composite switch (all) instead of the single band switches. 
The switches offer additional state info to supervise the current switch progress.

The Wi-Fi switches offer the following state information

| Name              | Values                 | Description                                                                                       |
|-------------------|------------------------|---------------------------------------------------------------------------------------------------|
| `state`           | `on` or `off`          | Switch state.                                                                                     |
| `switch_progress` | `on`, `off` or `error` | Whether a switch change is in progress or not or `error` if the last switch operation was faulty. |

### Sensor & Binary sensor 
The component offers various sensors:

| Entity                                                | Description                       |
|-------------------------------------------------------|-----------------------------------|
| binary_sensor.compal_wifi_modem_guest_wifi            | Guest Wifi state                  |
| binary_sensor.compal_wifi_modem_internet_connectivity | Modem internet connectivity state |
| binary_sensor.compal_wifi_modem_telephone_line_1      | Telephone line 1 state            |
| binary_sensor.compal_wifi_modem_telephone_line_2      | Telephone line 2 state            |
| sensor.compal_wifi_modem_last_poll                    | Timestamp of last status poll     |
| sensor.compal_wifi_modem_model                        | Modem model                       |
| sensor.compal_wifi_modem_hardware_version             | Hardware version                  |
| sensor.compal_wifi_modem_software_version             | Software version                  |
| sensor.compal_wifi_modem_operator                     | Modem operator                    |
| sensor.compal_wifi_modem_uptime                       | Modem uptime                      |

## Services
The component offers the following services:

| Name                 | Description                                |
|----------------------|--------------------------------------------|
| compal_wifi.poll_now | Polls the status of the modem immediately. |
| compal_wifi.reboot   | Reboots the modem.                         |

## Integration
The integration with the compal modem is done using [compal-wifi-switch][compal-wifi-switch].  

[hacs-shield]: https://img.shields.io/badge/HACS-Default-41BDF5.svg
[hacs]: https://github.com/hacs/integration
[downloads-latest-shield]:https://img.shields.io/github/downloads/frimtec/hass-compal-wifi/latest/total
[downloads-shield]:https://img.shields.io/github/downloads/frimtec/hass-compal-wifi/total
[maintenance-shield]: https://img.shields.io/maintenance/no/2023.svg
[license-shield]: https://img.shields.io/github/license/frimtec/hass-compal-wifi.svg
[license]: https://opensource.org/licenses/Apache-2.0
[build-status-shield]: https://github.com/frimtec/hass-compal-wifi/actions/workflows/build.yml/badge.svg
[build-status]: https://github.com/frimtec/hass-compal-wifi/actions/workflows/build.yml
[deploy-status-shield]: https://github.com/frimtec/hass-compal-wifi/actions/workflows/deploy_release.yml/badge.svg
[deploy-status]: https://github.com/frimtec/hass-compal-wifi/actions/workflows/deploy_release.yml
[latest-release]: https://github.com/frimtec/hass-compal-wifi/releases/latest
[compal-wifi-switch]: https://github.com/frimtec/compal-wifi-switch
