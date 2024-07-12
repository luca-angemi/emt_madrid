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

from .const import CONF_STOP_ID, DOMAIN
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
    lines = coordinator.data["lines"]
    sensors = [
        EMTMadridSensor(config_entry, SENSOR_TYPE_EMT[0], coordinator, line) for line in lines]
    async_add_entities(sensors)


class EMTMadridSensor(AirFryerEntity, SensorEntity):
    """EMT Madrid Sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        description: SensorEntityDescription,
        coordinator,
        line,
    ) -> None:
        """Initialize a EMT Madrid sensor."""
        super().__init__(config_entry, description, coordinator)
        self.entity_description = description
        self.line = line
        self._attr_name = "Bus " + line + " Next Arrival"
        self._attr_unique_id = slugify(
            DOMAIN + config_entry.data[CONF_STOP_ID] + line
        )
    @property
    def native_value(self):
        """Return the state."""
    def native_value(self):
        """Return the state."""
        if self.coordinator.data and self.coordinator.data["lines"][self.line]["arrivals"]:
            return self.coordinator.data["lines"][self.line]["arrivals"][0]
