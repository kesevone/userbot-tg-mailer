import re
from datetime import timedelta
from typing import Optional

from pytils.numeral import get_plural


def str2timedelta(time: str) -> Optional[timedelta]:
    """Convert a string representation of a time interval to a datetime object.

    Parameters:
        time (str): A string representation of a time interval, e.g. "2d 4h 30m".

    Returns:
        Optional[timedelta]: A datetime.timedelta object if the input string is
            a valid time interval, else None.

    Examples:
        >>> str2timedelta('1d 2h 30m')
        'timedelta(days=1, hours=2, minutes=30)'
    """
    try:
        days = int(re.search(r"(\d+)d", time).group(1))
        hours = int(re.search(r"(\d+)h", time).group(1))
        minutes = int(re.search(r"(\d+)m", time).group(1))

        return timedelta(days=days, hours=hours, minutes=minutes)
    except:
        return None


def timedelta2str(td: timedelta, short: bool = False) -> str | int:
    """
    Convert a timedelta object to a human-friendly string representation.

    Parameters:
        td (timedelta): The timedelta object to convert.
        short (bool, optional): If True, return a shorter, more concise
            representation. Defaults to False.

    Returns:
        str | int: A human-friendly string representation of the timedelta
            object.

    Examples:
        >>> timedelta2str(timedelta(days=1, hours=2, minutes=3))
        '1 day 2 hours 3 minutes'
    """
    try:
        days = td.days
        hours = td.seconds // 3600
        minutes = (td.seconds // 60) % 60
        td_strings = []

        if short:
            if days != 0:
                td_strings.append("{days}d. ".format(days=days))
            if hours != 0:
                td_strings.append("{hours}h. ".format(hours=hours))
            if minutes != 0:
                td_strings.append("{minutes}m.".format(minutes=minutes))
        else:
            if days != 0:
                td_strings.append(get_plural(days, "day, day, days"))
            if hours != 0:
                td_strings.append(get_plural(hours, "hour, hour, hours"))
            if minutes != 0:
                td_strings.append(get_plural(minutes, "minute, minute, minutes"))

        return " ".join(td_strings)
    except:
        return None
