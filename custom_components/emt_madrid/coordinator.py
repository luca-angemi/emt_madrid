"""Coordinator for EMT Madrid."""

from datetime import timedelta
import logging

from emt_madrid.domain.exceptions import EMTError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

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

    async def _async_update_data(self):
        try:
            return await async_get_api_emt_instance(
                self.hass, self.config_entry.options
            )
        except EMTError as err:
            raise UpdateFailed(f"EMT API error: {err}") from err
