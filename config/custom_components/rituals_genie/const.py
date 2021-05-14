"""Constants for Rituals Genie."""
# Base component constants
NAME = "Rituals Genie"
MANUFACTURER = "Rituals"
MODEL = "Genie"
DOMAIN = "rituals_genie"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/fred-oranje/rituals-genie/issues"

# Icons
ICON = "mdi:format-quote-close"
ICON_WIFI = "mdi:wifi"
ICON_PERFUME = "mdi:nfc-variant"
ICON_FAN = "mdi:fan"
ICON_FILL = "mdi:format-color-fill"

# Platforms
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [SENSOR, SWITCH]

# Configuration and options
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_HUB_HASH = "hub_hash"
CONF_HUB_NAME = "hub_name"
CONF_WIFI_SENSOR_ENABLED = "wifi_enabled"
CONF_PERFUME_SENSOR_ENABLED = "perfume_enabled"
CONF_FILL_SENSOR_ENABLED = "fill_enabled"
CONF_SWITCH_ENABLED = "switch_enabled"

# Defaults
DEFAULT_NAME = "Rituals Genie"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
