"""
Time conversions for use with the scheduler
"""
import logging


def minutes_to_seconds(minutes):
    """
    Converts minutes to seconds
    :param minutes: Minutes passed in
    :return: How long minutes are in seconds
    """
    return int(minutes) * 60


def hours_to_minutes(hours):
    """
    Converts hours to minutes
    :param hours: Hours to be converted
    :return: Equivalent value of hours in minutes
    """
    return int(hours) * 60


def hhmm_to_seconds(hhmm):
    """
    Converts time in hhmm format into number of seconds
    :param hhmm: The time format to be converted to seconds
    :return: Seconds equivalent to hhmm argument
    """
    if len(hhmm.split(':')) != 2:
        logging.warning('Wrong format for passing in time')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
           minutes_to_seconds(hhmm.split(':')[1])
