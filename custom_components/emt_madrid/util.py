"""Util for the EMT Madrid integration."""

import logging

from aiohttp import ClientSession

from emt_madrid import EMTClient
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import CONF_STOP_IDS

logging.getLogger("emt_madrid").setLevel(logging.ERROR)

async def async_get_api_emt_instance(data):
    """Get EMT data for all requested stop IDs using the new EMTClient."""
    async with ClientSession() as session:
        # Crea i client per ogni fermata
        stops = {}
        for stop_id in data[CONF_STOP_IDS]:
            client = EMTClient(
                email=data[CONF_USERNAME],
                password=data[CONF_PASSWORD],
                stop_id=stop_id,
                session=session,
            )
            stop = await client.get_arrivals()

            stops[stop_id] = {
                "stop_coordinates": stop.stop_coordinates,
                "lines": {
                    line.line_number: {
                        "arrivals": list(filter(None, [line.arrival, line.next_arrival]))
                    }
                    for line in stop.stop_lines
                }
            }
        return stops
