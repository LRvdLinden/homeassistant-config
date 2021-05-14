"""Adds config flow for Rituals Genie."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import RitualsGenieApiClient
from .const import CONF_FILL_SENSOR_ENABLED
from .const import CONF_HUB_HASH
from .const import CONF_HUB_NAME
from .const import CONF_PASSWORD
from .const import CONF_PERFUME_SENSOR_ENABLED
from .const import CONF_SWITCH_ENABLED
from .const import CONF_USERNAME
from .const import CONF_WIFI_SENSOR_ENABLED
from .const import DOMAIN


class RitualsGenieFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for rituals_genie."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            hubs = await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )
            if not hubs:
                self._errors["base"] = "auth"
            else:
                self._hubs_info = hubs

                return await self.async_step_hub()

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def async_step_hub(self, user_input=None):
        """Handle second step in the user flow"""
        self._errors = {}

        if user_input is not None:
            # Find the hub
            hub_hash = None
            hub_name = None
            for hub in self._hubs_info:
                name = hub.get("hub").get("attributes").get("roomnamec")[0]
                if name == user_input[CONF_HUB_NAME]:
                    hub_name = name
                    hub_hash = hub.get("hub").get("hash")
                    break

            if hub_hash is None:
                self._errors["base"] = "invalid_hub"
            else:
                return self.async_create_entry(
                    title=hub_name,
                    data={
                        CONF_HUB_NAME: hub_name,
                        CONF_HUB_HASH: hub_hash,
                    },
                )

            return await self._show_hubs_config_form(self._hubs_info, user_input)

        return await self._show_hubs_config_form(self._hubs_info, user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return RitualsGenieOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit username / password data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=self._errors,
        )

    async def _show_hubs_config_form(
        self, hubs, user_input
    ):  # pylint: disable=unused-argument
        """Show the configuration form to choose hub"""
        hub_names = []
        for hub in hubs:
            name = hub.get("hub").get("attributes").get("roomnamec")[0]
            try:
                hub_names.index(name)
            except ValueError:
                hub_names.append(name)
                pass

        return self.async_show_form(
            step_id="hub",
            data_schema=vol.Schema({vol.Required(CONF_HUB_NAME): vol.In(hub_names)}),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = RitualsGenieApiClient("", session)
            return await client.async_get_hubs(username, password)
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class RitualsGenieOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for rituals_genie."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PERFUME_SENSOR_ENABLED,
                        default=self.options.get(CONF_PERFUME_SENSOR_ENABLED, True),
                    ): bool,
                    vol.Required(
                        CONF_FILL_SENSOR_ENABLED,
                        default=self.options.get(CONF_FILL_SENSOR_ENABLED, True),
                    ): bool,
                    vol.Required(
                        CONF_WIFI_SENSOR_ENABLED,
                        default=self.options.get(CONF_WIFI_SENSOR_ENABLED, True),
                    ): bool,
                    vol.Required(
                        CONF_SWITCH_ENABLED,
                        default=self.options.get(CONF_SWITCH_ENABLED, True),
                    ): bool,
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_HUB_NAME), data=self.options
        )
