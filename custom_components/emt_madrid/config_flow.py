"""Config flow for EMT Madrid integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_STOP_IDS, DOMAIN
from .util import async_get_api_emt_instance

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STOP_IDS): SelectSelector(
            SelectSelectorConfig(
                options=[],
                multiple=True,
                custom_value=True,
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    stop_info = await async_get_api_emt_instance(hass, data)
    if not stop_info:
        raise InvalidAuth

    return {"title": "EMT Madrid"}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EMT Madrid."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data={},
                    options=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class OptionsFlowHandler(OptionsFlow):
    """Config flow options handler for EMT Madrid."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            entity_registry = er.async_get(self.hass)
            device_registry = dr.async_get(self.hass)
            entries = er.async_entries_for_config_entry(
                entity_registry, self._config_entry_id
            )
            removed_devices = set()

            for entry in entries:
                if entry.unique_id.split("_")[2] not in user_input[CONF_STOP_IDS]:
                    entity_registry.async_remove(entry.entity_id)
                    removed_devices.add(entry.device_id)

            for device_id in removed_devices:
                device_registry.async_remove_device(device_id)

            options = dict(self.config_entry.options)
            options.update(user_input)
            return self.async_create_entry(title="", data=options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_STOP_IDS, default=self.config_entry.options[CONF_STOP_IDS]
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[],
                            multiple=True,
                            custom_value=True,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
        )
