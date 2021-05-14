"""Sample API Client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

TIMEOUT = 10
API_URL = "https://rituals.sense-company.com"

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class RitualsGenieApiClient:
    def __init__(self, hub_hash: str, session: aiohttp.ClientSession) -> None:
        """Rituals API Client."""
        self._hub_hash = hub_hash
        self._session = session

    async def async_get_hubs(self, username: str, password: str) -> list:
        """Login using the API"""
        url = API_URL + "/ocapi/login"
        response = await self.api_wrapper(
            "post", url, data={"email": username, "password": password}, headers=HEADERS
        )

        if response["account_hash"] is None:
            raise Exception("Authentication failed")
        else:
            _account_hash = response["account_hash"]

        """Retrieve hubs"""
        url = API_URL + "/api/account/hubs/" + _account_hash
        response = await self.api_wrapper("get", url)

        return response

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = API_URL + "/api/account/hub/" + self._hub_hash
        return await self.api_wrapper("get", url)

    async def async_set_on_off(self, value: bool) -> None:
        """Get data from the API."""
        if value is True:
            fanc = "1"
        else:
            fanc = "0"
        url = (
            API_URL
            + "/api/hub/update/attr?hub="
            + self._hub_hash
            + "&json=%7B%22attr%22%3A%7B%22fanc%22%3A%22"
            + fanc
            + "%22%7D%7D"
        )

        await self.api_wrapper("postnonjson", url)

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                    return await response.json()

                elif method == "postnonjson":
                    return await self._session.post(url)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
