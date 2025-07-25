"""Entity representing a EMT Madrid device."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class AirFryerEntity(CoordinatorEntity):
    """Representation of a EMT Madrid entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        config_entry: ConfigEntry,
        description: EntityDescription,
        coordinator,
    ) -> None:
        """Initialize a D-Link Power Plug entity."""
        super().__init__(coordinator)
