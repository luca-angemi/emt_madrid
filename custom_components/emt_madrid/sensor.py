"""Sensors of the EMT Madrid component."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify

from .const import DOMAIN
from .entity import AirFryerEntity

_LOGGER = logging.getLogger(__name__)


SENSOR_TYPE_EMT: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="next_arrival",
        translation_key="arrival",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up the EMT Madrid sensor."""
    coordinator = config_entry.runtime_data
    entities = [
        EMTMadridSensor(config_entry, SENSOR_TYPE_EMT[0], coordinator, line, stop_id)
        for stop_id in list(coordinator.lines.keys())
        for line in coordinator.lines[stop_id]
    ]

    async_add_entities(entities)


class EMTMadridSensor(AirFryerEntity, SensorEntity):
    """EMT Madrid Sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        description: SensorEntityDescription,
        coordinator,
        line,
        stop_id,
    ) -> None:
        """Initialize a EMT Madrid sensor."""
        super().__init__(config_entry, description, coordinator)
        self.entity_description = description
        self.line = line
        self.stop_id = stop_id
        self._attr_extra_state_attributes = {"stop_id": stop_id}
        self._attr_name = "Bus " + line + " Next Arrival"
        self._attr_unique_id = slugify(DOMAIN + " " + stop_id + " " + line,separator="_")

    @property
    def native_value(self):
        """Return the state."""
        data = self.coordinator.data
        try:
            return data[self.stop_id]["lines"][self.line]["arrivals"][0]
        except (KeyError, TypeError):
            return None
