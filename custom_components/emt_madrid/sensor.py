"""Sensors of the EMT Madrid component."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import EMTCoordinator

_LOGGER = logging.getLogger(__name__)


SENSOR_TYPE_EMT: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="next_arrival",
        translation_key="arrival",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    """Set up the EMT Madrid sensor."""
    coordinator = config_entry.runtime_data
    entities = [
        EMTMadridSensor(SENSOR_TYPE_EMT[0], coordinator, line_number, stop_id)
        for stop_id, stop_data in coordinator.data.items()
        for line_number in stop_data.get("lines", {})
    ]

    async_add_entities(entities)


class EMTMadridSensor(CoordinatorEntity[EMTCoordinator], SensorEntity):
    """EMT Madrid Sensor."""

    def __init__(
        self,
        description: SensorEntityDescription,
        coordinator,
        line,
        stop_id,
    ) -> None:
        """Initialize a EMT Madrid sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self.line = line
        self.stop_id = stop_id
        self._attr_name = "Bus stop " + stop_id + " line " + line + " Next Arrival"
        self._attr_unique_id = slugify(
            DOMAIN + " " + stop_id + " " + line, separator="_"
        )
        self._device_id = "emt_madrid_bus_stop_" + stop_id
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            entry_type=dr.DeviceEntryType.SERVICE,
            name="Bus Stop " + stop_id,
        )
        lon, lat = coordinator.data[stop_id]["stop_coordinates"]
        self._attr_extra_state_attributes = {"latitude": lat, "longitude": lon}

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        value = self.coordinator.data[self.stop_id]["lines"][self.line]["arrivals"][0]
        return min(value, 45)

    @property
    def available(self) -> bool:
        """Return the state."""
        return (
            self.stop_id in self.coordinator.data
            and self.line in self.coordinator.data[self.stop_id].get("lines", {})
            and self.coordinator.data[self.stop_id]["lines"][self.line]["arrivals"]
        )
