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

    api = await async_get_api_emt_instance(entry.options)
    coordinator = EMTCoordinator(hass, api)
    await coordinator.async_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EMTConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: EMTConfigEntry) -> None:
    """Handle an options update."""
    await hass.config_entries.async_reload(entry.entry_id)
