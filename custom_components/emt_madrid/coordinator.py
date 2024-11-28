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

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.lines = {}

    async def _async_update_data(self):
        """Fetch data from EMT Madrid API."""
        stops = await async_get_api_emt_instance(self.config_entry.options)
        stop_info = {}
        for stop, info in stops.items():
            stop_info[stop] = info.get_stop_info()
            self.lines[stop] = list(stop_info[stop]["lines"].keys())
        return stop_info
