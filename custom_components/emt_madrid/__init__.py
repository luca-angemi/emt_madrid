"""The EMT Madrid integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import EMTCoordinator
from .util import async_get_api_emt_instance

PLATFORMS: list[Platform] = [Platform.SENSOR]

type EMTConfigEntry = ConfigEntry[EMTCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: EMTConfigEntry) -> bool:
    """Set up EMT Madrid from a config entry."""

    api = await async_get_api_emt_instance(entry.data)
    coordinator = EMTCoordinator(hass, api)
    await coordinator.async_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: EMTConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
