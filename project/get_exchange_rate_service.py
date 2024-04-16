from datetime import datetime
from typing import Optional

import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class GetExchangeRateResponse(BaseModel):
    """
    Provides the exchange rate for a specified currency pair along with the date of the rate.
    """

    base_currency: str
    target_currency: str
    exchange_rate: float
    date: str


async def get_exchange_rate(
    base_currency: str, target_currency: str, date: Optional[str]
) -> GetExchangeRateResponse:
    """
    Retrieves the latest exchange rates for specified currency pairs.

    Args:
    base_currency (str): The code of the base currency for which the exchange rate is being requested (e.g., USD).
    target_currency (str): The code of the target currency for the conversion (e.g., EUR).
    date (Optional[str]): Optional date for retrieving historical exchange rates. If not provided, the most recent rate is used.

    Returns:
    GetExchangeRateResponse: Provides the exchange rate for a specified currency pair along with the date of the rate.
    """
    rate_record = await prisma.models.APIRequest.prisma().find_first(
        where={
            "endpoint": f"{base_currency}_TO_{target_currency}",
            "createdAt": datetime.strptime(date, "%Y-%m-%d")
            if date
            else datetime.now(),
        },
        order={"createdAt": "desc"},
    )
    if rate_record:
        return GetExchangeRateResponse(
            base_currency=base_currency,
            target_currency=target_currency,
            exchange_rate=rate_record.responseBody["rate"],
            date=date or datetime.now().strftime("%Y-%m-%d"),
        )
    api_url = f"https://api.exchangerate.host/convert?from={base_currency}&to={target_currency}&date={date or 'latest'}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
    response_data = response.json()
    await prisma.models.APIRequest.prisma().create(
        data={
            "endpoint": f"{base_currency}_TO_{target_currency}",
            "requestBody": {"from": base_currency, "to": target_currency, "date": date},
            "responseBody": {"rate": response_data["info"]["rate"]},
            "apiKey": {
                "connectOrCreate": {
                    "create": {
                        "key": "DUMMY_API_KEY_FOR_DEMO_PURPOSES",
                        "userId": "SOME_USER_ID",
                    },
                    "where": {"key": "DUMMY_API_KEY_FOR_DEMO_PURPOSES"},
                }
            },
        }
    )
    return GetExchangeRateResponse(
        base_currency=base_currency,
        target_currency=target_currency,
        exchange_rate=response_data["info"]["rate"],
        date=response_data["date"],
    )
