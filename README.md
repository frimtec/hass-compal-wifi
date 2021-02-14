# Compal WiFi integration for Home Assistant

Home Assistant component to switch WiFi on or off of the modem Compal CH7465LG.

The component is tested with the modem firmware version ```CH7465LG-NCIP-6.15.28-4p8-NOSH```.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory create a new folder called `compal-wifi`.
4. Download _all_ the files from the `custom_components/compal-wifi/` directory in this repository.
5. Place the files you downloaded in the new directory you created.
6. Move on to the configuration in the file `configuration.yaml`.
7. Restart Home Assistant.

## Configuration 
 
Add a configuration to your `configuration.yaml` file:
``` yaml
compal_wifi:
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

## Services
The compntent offers the following services:

Name | Paramtername | Parameter values | Description
---- | ------------ | ---------------- | -----------
`compal_wifi.wifi_on` | `radio` | `2g`, `5g` or `all` | Switches on the selected WiFI band.
`compal_wifi.wifi_off` | `radio` | `2g`, `5g` or `all` | Switches off the selected WiFI band.

## Platforms

### Binary Sensor
Work in progress.

### Switch
Work in progress.
