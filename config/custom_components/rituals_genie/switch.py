"""Switch platform for Rituals Genie."""
from homeassistant.components.switch import SwitchEntity

from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON_FAN
from .entity import RitualsGenieEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([RitualsGenieBinarySwitch(coordinator, entry, "")])


class RitualsGenieBinarySwitch(RitualsGenieEntity, SwitchEntity):
    """rituals_genie switch class."""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.async_set_on_off(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.async_set_on_off(False)
        await self.coordinator.async_request_refresh()

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{DEFAULT_NAME} {self.hub_name}"

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON_FAN

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return (
            self.coordinator.data.get("hub").get("attributes").get("fanc", "0") == "1"
        )
