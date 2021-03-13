# Compal WiFi integration for Home Assistant
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

[![Build](https://github.com/frimtec/hass-compal-wifi/actions/workflows/build.yml/badge.svg)](https://github.com/frimtec/hass-compal-wifi/actions/workflows/build.yml)
[![Deploy release](https://github.com/frimtec/hass-compal-wifi/actions/workflows/deploy_release.yml/badge.svg)](https://github.com/frimtec/hass-compal-wifi/actions/workflows/deploy_release.yml)

![Icon](images/icon-readme.png) ![WiFi switches!](images/compal-wifi.png)

Home Assistant component to switch WiFi of the modem Compal CH7465LG on or off.
The component is tested with the modem firmware version ```CH7465LG-NCIP-6.15.28-4p8-NOSH```.

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
switch:
  - platform: compal_wifi
    host: 192.168.0.1
    password: YOUR_PASSWORD
```

### Configuration options

Key | Type | Required | Description
--- | ---- | -------- | -----------
`host` | `string` | `True` | The hostname or IP address of your compal modem, e.g., 192.168.0.1.
`password` | `string` | `True` | The password for your modems administration account.
`guest_macs_2g` | `string[]` | `False` | List of guest MAC addresses to enable when switching ON 2G WiFi band. 
`guest_macs_5g` | `string[]` | `False` | List of guest MAC addresses to enable when switching ON 5G WiFi band.
`pause` | `int` | `False` | Number of seconds to wait between modem changes (default 60s).


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

## Integration
The integration with the compal modem is done using [compal-wifi-switch](https://github.com/frimtec/compal-wifi-switch).  
