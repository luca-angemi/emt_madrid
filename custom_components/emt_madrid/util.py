"""Util for the EMT Madrid integration."""

import asyncio
import logging

from aiohttp import ClientSession
from emt_madrid import EMTClient

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import CONF_STOP_IDS

logging.getLogger("emt_madrid").setLevel(logging.ERROR)


async def async_get_api_emt_instance(data):
    """Get an instance of the EMT API client."""
    async with ClientSession() as session:

        async def fetch_stop(stop_id):
            client = EMTClient(
                email=data[CONF_USERNAME],
                password=data[CONF_PASSWORD],
                stop_id=stop_id,
                session=session,
            )
            stop = await client.get_arrivals()
            return stop_id, {
                "stop_coordinates": stop.stop_coordinates,
                "lines": {
                    line.line_number: {
                        "arrivals": list(
                            filter(None, [line.arrival, line.next_arrival])
                        )
                    }
                    for line in stop.stop_lines
                },
            }

        tasks = [fetch_stop(stop_id) for stop_id in data[CONF_STOP_IDS]]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        stops = {}
        for result in results:
            if isinstance(result, Exception):
                continue
            stop_id, stop_data = result
            stops[stop_id] = stop_data

        return stops
