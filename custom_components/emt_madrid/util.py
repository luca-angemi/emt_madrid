"""Util for the EMT Madrid integration."""

import logging

from aiohttp import ClientSession

from emt_madrid import EMTAPIAuthenticator, EMTAPIBusStop
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import CONF_STOP_IDS

logging.getLogger("emt_madrid.emt_api").setLevel(logging.ERROR)


async def async_get_api_emt_instance(data):
    """Get API EMT api response."""
    async with ClientSession() as session:
        emt_api_authenticator = EMTAPIAuthenticator(
            session, data[CONF_USERNAME], data[CONF_PASSWORD]
        )
        await emt_api_authenticator.authenticate()
        token = emt_api_authenticator.token
        emt_api_bus_stop = {}
        for stop_id in data[CONF_STOP_IDS]:
            emt_api_bus_stop[stop_id] = EMTAPIBusStop(session, token, stop_id)
            await emt_api_bus_stop[stop_id].update_stop_info()
            await emt_api_bus_stop[stop_id].update_bus_arrivals()
            emt_api_bus_stop[stop_id].get_stop_info()
        return emt_api_bus_stop
