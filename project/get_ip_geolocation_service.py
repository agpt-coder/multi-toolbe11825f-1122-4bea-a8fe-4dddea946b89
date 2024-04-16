from typing import Optional

import httpx
from pydantic import BaseModel


class GeoLocationResponse(BaseModel):
    """
    Outputs the geolocation details for the requested IP address, including country, region, city, and potentially more.
    """

    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    zipcode: Optional[str] = None
    timezone: str
    isp: str
    organization: Optional[str] = None


async def get_ip_geolocation(ip: str) -> GeoLocationResponse:
    """
    Retrieves geolocation data for a given IP address using an external IP Geolocation API.

    Args:
        ip (str): The IP address for which geolocation data is being requested.

    Returns:
        GeoLocationResponse: Outputs the geolocation details for the requested IP address, including country, region, city, and potentially more.

    Example:
        ip_info = await get_ip_geolocation('8.8.8.8')
        print(ip_info)
    """
    GEOLOCATION_API_URL = (
        "https://api.ipgeolocation.io/ipgeo?apiKey=YOUR_API_KEY&ip=" + ip
    )
    async with httpx.AsyncClient() as client:
        response = await client.get(GEOLOCATION_API_URL)
        data = response.json()
        return GeoLocationResponse(
            country=data.get("country_name", ""),
            region=data.get("state_prov", ""),
            city=data.get("city", ""),
            latitude=float(data.get("latitude", 0)),
            longitude=float(data.get("longitude", 0)),
            zipcode=data.get("zipcode", None),
            timezone=data.get("time_zone", ""),
            isp=data.get("isp", ""),
            organization=data.get("organization", None),
        )
