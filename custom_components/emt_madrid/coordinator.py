"""Coordinator for EMT Madrid."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .util import async_get_api_emt_instance

_LOGGER = logging.getLogger(__name__)

class EMTCoordinator(DataUpdateCoordinator):
    """Class to manage fetching EMT Madrid data."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch data from EMT Madrid API."""
        bus_stop = await async_get_api_emt_instance(self.config_entry.data)
        return bus_stop.get_stop_info()

