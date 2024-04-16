from datetime import datetime

import pytz
from pydantic import BaseModel


class TimezoneConvertResponse(BaseModel):
    """
    Response model showing the converted timestamp and the target time zone details.
    """

    converted_timestamp: str
    source_timezone: str
    target_timezone: str


def convert_timezone(
    timestamp: str, source_timezone: str, target_timezone: str
) -> TimezoneConvertResponse:
    """
    Converts a timestamp from one time zone to another, adjusting for daylight saving time as necessary.

    Args:
        timestamp (str): The original timestamp to convert, in a standard format (e.g., ISO 8601).
        source_timezone (str): The time zone of the original timestamp (e.g., 'America/New_York').
        target_timezone (str): The target time zone for conversion (e.g., 'Europe/London').

    Returns:
        TimezoneConvertResponse: Response model showing the converted timestamp and the target time zone details.
    """
    source_tz = pytz.timezone(source_timezone)
    naive_datetime = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    localized_datetime = source_tz.localize(naive_datetime)
    target_tz = pytz.timezone(target_timezone)
    converted_datetime = localized_datetime.astimezone(target_tz)
    converted_timestamp_str = converted_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    return TimezoneConvertResponse(
        converted_timestamp=converted_timestamp_str,
        source_timezone=source_timezone,
        target_timezone=target_timezone,
    )
