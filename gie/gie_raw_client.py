import datetime
from typing import Optional, Union

import aiohttp as aiohttp

from gie.agsi_mappings import (
    AGSIFacility,
    AGSICountry,
    lookup_country_agsi,
    lookup_facility_agsi,
    AGSICompany, lookup_agsi_company,
)
from gie.alsi_mappings import (
    ALSIFacility,
    lookup_country_alsi,
    lookup_facility_alsi, lookup_alsi_company, ALSICompany,
)
from gie.api_mappings import APIType
from gie.exceptions import ApiError


class GieRawClient:
    def __init__(self, api_key: str, session: Optional[aiohttp.ClientSession] = None):
        self.api_key = api_key
        self.session = session

        if not self.session:
            self.session = aiohttp.ClientSession(
                raise_for_status=True, headers={"x-key": self.api_key}
            )

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value):
        if not value:
            raise ApiError("API token is missing!")
        self.__api_key = value

    async def query_agsi_eic_listing(self):
        return await self.fetch("/about?show=listing", APIType.AGSI)

    async def query_alsi_eic_listing(self):
        return await self.fetch("/about?show=listing", APIType.ALSI)

    async def query_alsi_news_listing(
            self, news_url_item: Optional[Union[int, str]] = None
    ):
        return await self.fetch("/news?", APIType.ALSI, news_url_item=news_url_item)

    async def query_agsi_news_listing(
            self, news_url_item: Optional[Union[int, str]] = None
    ):
        return await self.fetch("/news?", APIType.AGSI, news_url_item=news_url_item)

    # async def query_gas_storage(
    #     self,
    #     storage: Union[AGSIFacility, str],
    #     start: Optional[Union[datetime.datetime, str]] = None,
    #     end: Optional[Union[datetime.datetime, str]] = None,
    # ) -> Coroutine[Any, Any, None]:
    #     storage = lookup_storage_agsi(storage)
    #     return await self.fetch(storage.get_url(), APIType.AGSI, start=start, end=end)
    #
    # async def query_gas_company(
    #     self,
    #     company: Union[AGSICompany, str],
    #     start: Union[datetime.datetime, str],
    #     end: Union[datetime.datetime, str],
    # ) -> Coroutine[Any, Any, None]:
    #     company = lookup_company(company)
    #     return await self.fetch(company.get_url(), APIType.AGSI, start=start, end=end)
    #
    # async def query_gas_country(
    #     self,
    #     country: Union[AGSICountry, str],
    #     start: Union[datetime.datetime, str],
    #     end: Union[datetime.datetime, str],
    # ) -> Coroutine[Any, Any, None]:
    #     country = lookup_country_agsi(country)
    #     return await self.fetch(country.get_url(), APIType.AGSI, start=start, end=end)
    #
    # async def query_lng_terminal(
    #     self,
    #     terminal: Union[ALSIFacility, str],
    #     start: Union[datetime.datetime, str],
    #     end: Union[datetime.datetime, str],
    # ) -> Coroutine[Any, Any, None]:
    #     terminal = lookup_terminal(terminal)
    #     return await self.fetch(terminal.get_url(), APIType.ALSI, start=start, end=end)
    #
    # async def query_lng_lso(
    #     self,
    #     lso: Union[ALSICompany, str],
    #     start: Union[datetime.datetime, str],
    #     end: Union[datetime.datetime, str],
    # ) -> Coroutine[Any, Any, None]:
    #     lso = lookup_lso(lso)
    #     return await self.fetch(lso.get_url(), APIType.ALSI, start=start, end=end)
    #
    # async def query_lng_country(
    #     self,
    #     country: Union[ALSICountry, str],
    #     start: Union[datetime.datetime, str],
    #     end: Union[datetime.datetime, str],
    # ) -> Coroutine[Any, Any, None]:
    #     country = lookup_country_alsi(country)
    #     return await self.fetch(country.get_url(), APIType.ALSI, start=start, end=end)

    async def query_country_agsi_storage(
            self,
            country: Optional[Union[AGSICountry, str]] = None,
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        if country:
            country = lookup_country_agsi(country)
        return await self.fetch(
            country.get_url() if country else "",
            APIType.AGSI,
            start=start,
            end=end,
            date=date,
            size=size,
        )

    async def query_country_alsi_storage(
            self,
            country: Optional[Union[AGSICountry, str]] = None,
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        if country:
            country = lookup_country_alsi(country)
        return await self.fetch(
            country.get_url() if country else "",
            APIType.AGSI,
            start=start,
            end=end,
            date=date,
            size=size,
        )

    async def query_agsi_facility_storage(
            self,
            facility_name: Union[AGSIFacility, str],
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        if facility_name:
            facility_name = lookup_facility_agsi(facility_name)
        return await self.fetch(
            facility_name.get_url() if facility_name else "",
            APIType.AGSI,
            start=start,
            end=end,
            date=date,
            size=size,
        )

    async def query_alsi_facility_storage(
            self,
            facility_name: Union[ALSIFacility, str],
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        if facility_name:
            facility_name = lookup_facility_alsi(facility_name)
        return await self.fetch(
            facility_name.get_url() if facility_name else "",
            APIType.ALSI,
            start=start,
            end=end,
            date=date,
            size=size,
        )

    async def query_agsi_company(
            self,
            company_name: Union[AGSICompany, str],
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        company_name = lookup_agsi_company(company_name)
        return await self.fetch(company_name.get_url() if company_name else "", APIType.AGSI, start=start, end=end,
                                date=date, size=size)

    async def query_alsi_company(
            self,
            company_name: Union[ALSICompany, str],
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        company_name = lookup_alsi_company(company_name)
        return await self.fetch(company_name.get_url() if company_name else "", APIType.ALSI, start=start, end=end,
                                date=date, size=size)

    async def fetch(
            self,
            url: str,
            token: APIType,
            news_url_item: Optional[Union[int, str]] = None,
            start: Optional[Union[datetime.datetime, str]] = None,
            end: Optional[Union[datetime.datetime, str]] = None,
            date: Optional[Union[datetime.datetime, str]] = None,
            size: Optional[Union[int, str]] = None,
    ):
        par = {
            "url": news_url_item,
            "from": start,
            "to": end,
            "date": date,
            "size": size,
        }

        async with self.session.get(
                token.value + url, params={k: v for k, v in par.items() if v is not None}
        ) as resp:
            return await resp.json()

    async def close_session(self) -> None:
        """Close the session."""
        if self.session:
            await self.session.close()