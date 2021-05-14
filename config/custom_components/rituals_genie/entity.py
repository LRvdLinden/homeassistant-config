"""RitualsGenieEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import CONF_HUB_NAME
from .const import DOMAIN
from .const import MANUFACTURER
from .const import MODEL
from .const import NAME


class RitualsGenieEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry, sensor_name):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.sensor_name = sensor_name
        self.hub_name = config_entry.data.get(CONF_HUB_NAME)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.hub_name}_{self.sensor_name}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": f"{NAME} {self.hub_name}",
            "model": MODEL,
            "manufacturer": MANUFACTURER,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }
