"""
Time conversions for use with the scheduler
"""
import logging
import time


def time_difference(scheduled_time):
    """
    Will calculate difference between current time and scheduled time in seconds
    :param scheduled_time: Time passed in url query
    :return: Difference between times in seconds or None if invalid entry
    """
    # Checks scheduled time is in the correct format
    parts = scheduled_time.split(":")
    if len(parts) != 2:
        logging.warning('Wrong format for passing in time')
        return None
    if not parts[0].isnumeric() and not parts[1].isnumeric():
        logging.warning('Time must be an integer')
        return None
    if int(parts[0]) > 23:
        logging.warning('Hour format for scheduled time is too big')
        return None
    if int(parts[1]) > 59:
        logging.warning('Minute format for scheduled time is too big')
        return None
    if int(parts[0]) < 0:
        logging.warning('Hour format for scheduled time is too small')
        return None
    if int(parts[1]) < 0:
        logging.warning('Minute format for scheduled time is too small')
        return None
    hour_time_dif = int(scheduled_time.split(":")[0]) - time.gmtime().tm_hour
    # Will calculate how many hours until the scheduled time
    if hour_time_dif < 0:
        hour_time_dif += 24
    min_time_dif = int(scheduled_time.split(":")[1]) - time.gmtime().tm_min
    # Will calculate how many minutes until the scheduled minute
    if min_time_dif < 0:
        min_time_dif += 60
    # Will check if time is the
    if hour_time_dif == 0 and min_time_dif == 0:
        return 24*60*60
    else:
        total_seconds = hour_time_dif*60*60 + min_time_dif*60
        return total_seconds
