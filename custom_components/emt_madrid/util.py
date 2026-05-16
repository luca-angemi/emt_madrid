"""Util for the EMT Madrid integration."""

import asyncio

from emt_madrid import EMTClient
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STOP_IDS

async def async_get_api_emt_instance(hass: HomeAssistant, data):
    """Get an instance of the EMT API client."""
    session = async_get_clientsession(hass)

    async def fetch_stop(stop_id):
        client = EMTClient(
            email=data[CONF_USERNAME],
            password=data[CONF_PASSWORD],
            stop_id=stop_id,
            session=session,
        )
        stop = await client.get_arrivals()

        bus_coords_by_line = {}

        for line in stop.stop_lines:
            buses = [
                b for b in stop.bus_arrivals
                if b.line == line.line_number and b.estimate_arrive_sec is not None
            ]

            if not buses:
                bus_coords_by_line[line.line_number] = None
                continue

            first_bus = min(
                buses,
                key=lambda b: b.estimate_arrive_sec
            )

            bus_coords_by_line[line.line_number] = first_bus.coordinates

        return stop_id, {
            "stop_coordinates": stop.stop_coordinates,
            "lines": {
                line.line_number: {
                    "arrivals": [
                        arr
                        for arr in [line.arrival, line.next_arrival]
                        if arr is not None
                    ],
                    "bus_coords": bus_coords_by_line.get(line.line_number),
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
