# Compal WiFi integration for Home Assistant
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

[![Build](https://github.com/frimtec/hass-compal-wifi/actions/workflows/build.yml/badge.svg)](https://github.com/frimtec/hass-compal-wifi/actions/workflows/build.yml)
[![Deploy release](https://github.com/frimtec/hass-compal-wifi/actions/workflows/deploy_release.yml/badge.svg)](https://github.com/frimtec/hass-compal-wifi/actions/workflows/deploy_release.yml)

![Icon](images/icon-readme.png)

Home Assistant component to switch WiFi of the modem Compal CH7465LG on or off.
The component is tested with the modem firmware version ```NCIP-6.15.30-1p3-1-NOSH```.

![WiFi switches!](images/compal-wifi.png)

This component is not official, developed, supported or endorsed by Compal.

## Installation

1. Using the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory there, you need to create it.
3. Create an empty directory `compal_wifi` inside the directory `custom_components`.
4. Download the ZIP archive `compal_wifi.zip` from the [latest release assets](https://github.com/frimtec/hass-compal-wifi/releases/latest).   
5. Extract the downladed ZIP archive to the directiry `custom_components/compal_wifi`.
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

Key | Type | Required | Description
--- | ---- | -------- | -----------
`host` | `string` | `True` | The hostname or IP address of your compal modem, e.g., 192.168.0.1.
`password` | `string` | `True` | The password for your modems administration account.
`guest` | `bool` | `False` | Enable guest network when switching ON WIFI. 
`pause` | `int` | `False` | Number of seconds to wait between modem changes (default 60s).
`polling_interval` | `int` | `False` | Number of seconds to poll modem state (default 3600s - 1h).


## Platforms

### Switch
The componet offers three switches to turn WiFi bands on or off:

Entity | Description
------ | -----------
`switch.wifi_2g` | Switch for 2.4 GHz WiFi band.
`switch.wifi_5g` | Switch for 5 GHz WiFi band.
`switch.wifi_all` | Switch for both WiFi bands. 

Be aware, swiching WiFi bands on or off are slow operations. If you want to switch all bands on or off better use the
composit switch (all) instead of the single band switches. 
The switches offer additional state info to supervise the current switch progess.

The WiFi switches offer the following state information

Name | Values | Description
---- | ------ | -----------
`state` | `on` or `off` | Switch state.
`switch_progress` | `on`, `off` or `error` | Whether a swich change is in progress or not or `error` if the last switch operation was faulty.

### Sensor & Binary sensor 
The componet offers various sensors:

Entity | Description
---- | -----------
binary_sensor.compal_wifi_modem_guest_wifi | Guest Wifi state
binary_sensor.compal_wifi_modem_internet_connectivity | Modem internet connectivity state
binary_sensor.compal_wifi_modem_telephone_line_1 | Telephone line 1 state
binary_sensor.compal_wifi_modem_telephone_line_2 | Telephone line 2 state
sensor.compal_wifi_modem_last_poll | Timestamp of last status poll
sensor.compal_wifi_modem_model | Modem model
sensor.compal_wifi_modem_hardware_version | Hardware version
sensor.compal_wifi_modem_software_version | Software version
sensor.compal_wifi_modem_operator | Modem operator
sensor.compal_wifi_modem_uptime | Modem uptime

## Services
The componet offers the following services:

Name | Description
---- | -----------
compal_wifi.poll_now | Polls the status of the modem immediatly.
compal_wifi.reboot | Reboots the modem.

## Integration
The integration with the compal modem is done using [compal-wifi-switch](https://github.com/frimtec/compal-wifi-switch).  
