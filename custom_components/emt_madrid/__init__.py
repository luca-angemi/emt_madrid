"""The EMT Madrid integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import EMTCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type EMTConfigEntry = ConfigEntry[EMTCoordinator]


async def async_setup_entry(hass: HomeAssistant, config_entry: EMTConfigEntry) -> bool:
    """Set up EMT Madrid from a config entry."""

    coordinator = EMTCoordinator(hass, config_entry)
    await coordinator.async_refresh()
    config_entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: EMTConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
