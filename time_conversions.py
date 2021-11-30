"""
Time conversions for use with the scheduler
"""
import logging


def mins_to_secs(minutes):
    """
    Converts minutes to seconds
    :param minutes: Minutes passed in
    :return: How long minutes are in seconds
    """
    return int(minutes) * 60


def hrs_to_mins(hours):
    """
    Converts hours to minutes
    :param hours: Hours to be converted
    :return: Equivalent value of hours in minutes
    """
    return int(hours) * 60


def hhmm_to_secs(hhmm):
    """
    Converts time in hhmm format into number of seconds
    :param hhmm: The time format to be converted to seconds
    :return: Seconds equivalent to hhmm argument
    """
    parts = hhmm.split(':')
    if len(parts) != 2:
        logging.warning('Wrong format for passing in time')
        return None
    return mins_to_secs(hrs_to_mins(parts[0])) + mins_to_secs(parts[1])
