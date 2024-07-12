"""Entity representing a D-Link Power Plug device."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class AirFryerEntity(CoordinatorEntity):
    """Representation of a D-Link Power Plug entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        config_entry: ConfigEntry,
        description: EntityDescription,
        coordinator,
    ) -> None:
        """Initialize a D-Link Power Plug entity."""
        super().__init__(coordinator)
        self._device_id = config_entry.entry_id
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            entry_type=dr.DeviceEntryType.SERVICE,
            name=config_entry.title,
        )
