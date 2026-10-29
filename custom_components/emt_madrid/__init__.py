"""The EMT Madrid integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import EMTCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type EMTConfigEntry = ConfigEntry[EMTCoordinator]


async def async_setup_entry(hass: HomeAssistant, config_entry: EMTConfigEntry) -> None:
    """Set up EMT Madrid from a config entry."""

    coordinator = EMTCoordinator(hass, config_entry)
    await coordinator.async_refresh()
    config_entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)


async def async_unload_entry(hass: HomeAssistant, config_entry: EMTConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
