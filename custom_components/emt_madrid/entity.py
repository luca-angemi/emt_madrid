"""Entity representing a EMT Madrid device."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class AirFryerEntity(CoordinatorEntity):
    """Representation of a EMT Madrid entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        config_entry: ConfigEntry,
        description: EntityDescription,
        coordinator,
    ) -> None:
        """Initialize a EMT Madrid entity."""
        super().__init__(coordinator)
        self._device_id = config_entry.unique_id
        self.entity_description = description
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=config_entry.title,
        )
