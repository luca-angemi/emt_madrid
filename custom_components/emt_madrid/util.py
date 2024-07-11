"""Util for the EMT Madrid integration."""
from aiohttp import ClientSession

from emt_madrid import EMTAPIAuthenticator, EMTAPIBusStop
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import CONF_STOP_ID


async def async_get_api_emt_instance(data):
    """Get API EMT api instance."""
    async with ClientSession() as session:
        emt_api_authenticator = EMTAPIAuthenticator(session, data[CONF_USERNAME], data[CONF_PASSWORD])
        await emt_api_authenticator.authenticate()
        token = emt_api_authenticator.token
        emt_api_bus_stop = EMTAPIBusStop(session, token, data[CONF_STOP_ID])
        await emt_api_bus_stop.update_stop_info()
        await emt_api_bus_stop.update_bus_arrivals()
        return emt_api_bus_stop #.get_stop_info()
