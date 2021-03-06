"""This is the main module which will deal with flask and the flow of the program
"""
import logging
from flask import Flask
from flask import render_template
from flask import request
import covid_data_handler
from covid_data_handler import get_starting_data
from covid_news_handling import update_news
from covid_news_handling import update_removed_news
from covid_news_handling import schedule_news_updates
from shared_data import get_covid_values
from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import set_news_articles
from shared_data import get_news_articles
from shared_data import set_scheduled_events
from decode_config import decode_config
from time_conversions import time_difference
from runtime_tests import schedule_tests


logging.basicConfig(filename='logging_file.log', level=logging.DEBUG)

# Default values are received for when the website is first opened
# Scheduler and app are also created here
articles = update_news()
set_news_articles(articles)
scheduled_events = []
set_scheduled_events(scheduled_events)
app = Flask(__name__)
location, _, nation_location, _, _, image_name = decode_config()

# Retrieves the starting covid data for the dashboard
get_starting_data()

# Runs tests
schedule_tests()


def check_updated_config():
    """This function will be scheduled to check if config file has been updated

    Will schedule itself every 5 minutes
    """
    global location, nation_location, image_name
    new_location, _, new_nation_location, _, _, new_image_name = decode_config()
    if (new_location, new_nation_location, new_image_name) != (location, nation_location,
                                                               image_name):
        location = new_location
        nation_location = new_nation_location
        image_name = new_image_name
        get_starting_data()
        logging.info("Config file updated")
    scheduler = get_scheduler()
    scheduler.enter(5 * 60, 1, check_updated_config, ())
    update_scheduler(scheduler)


# Checks for updated config file during runtime
check_updated_config()


def event_update(title: str, content: str, to_update: str, repeat: bool, test=False):
    """This procedure will add an event to the scheduled_events array

    This will be added to the left hand side of the webpage
    :param test: Checks whether test case is to be used (default false)
    :param repeat: Whether the event is to be repeated
    :param to_update: What is to be updated
    :param title: Title of the event
    :param content: Content displayed under the title
    :return: Only used in testing
    """
    if test:
        events = []
        events.append({'title': title, 'content': content,
                       'to_update': to_update, 'repeat': repeat})
        return events
    scheduled_events.append({'title': title, 'content': content,
                             'to_update': to_update, 'repeat': repeat})
    set_scheduled_events(scheduled_events)
    return scheduled_events


def remove_event(title: str):
    """Will remove event with the title provided from scheduled_events

    :param title: the title of the event to be removed
    """
    for event in scheduled_events:
        if event['title'] == title:
            scheduled_events.remove(event)
            set_scheduled_events(scheduled_events)
            break
    logging.error("No event found with that name")


def event_exists(title: str, test=False) -> bool:
    """Will cycle through events with the title provided from scheduled_events

    :param test: Checks whether test case is to be user (Default false)
    :param title: the title of the event to be removed
    :return True if event present otherwise False
    """
    present = False
    for event in scheduled_events:
        if event['title'] == title:
            present = True
    if test:
        events = [{'title': "test event", 'content': "test content",
                   'to_update': "both", 'repeat': False}]
        for event in events:
            if event['title'] == title:
                return True
        return False
    return present


def remove_news_from_home():
    """Changes articles when news has been removed so that the display can be updated
    """
    global articles
    articles = get_news_articles()


def add_update(repeat, data_to_update, news_to_update,
               label_name: str, scheduler_time: str) -> bool:
    """Will update both schedulers if both news and covid data are to be updated

    Will also deal if only one is to updated or neither
    :param repeat: Whether the event is to be repeated every 24 hours: Bool
    :param data_to_update: Whether the covid data is to be update: Bool
    :param news_to_update: Whether the news is to be update: Bool
    :param label_name: The name of the event to be added
    :param scheduler_time: The time the event is to be added
    :return: Return value to be used in testing
    """
    # Checks update interval is of a valid format
    update_interval = time_difference(scheduler_time)
    if update_interval is None:
        logging.info("Unable to schedule event due to invalid time format")
        return False
    # Checks what is to be updated
    # Then adds event to scheduled_events and adds to scheduler
    if data_to_update and news_to_update:
        event_update(label_name, scheduler_time, 'both', repeat)
        covid_data_handler.schedule_covid_updates(update_interval, label_name)
        schedule_news_updates(update_interval, label_name)
    elif data_to_update:
        event_update(label_name, scheduler_time, 'covid', repeat)
        covid_data_handler.schedule_covid_updates(update_interval, label_name)
    elif news_to_update:
        event_update(label_name, scheduler_time, 'news', repeat)
        schedule_news_updates(update_interval, label_name)
    else:
        logging.info('Nothing provided to update')
        return False
    return True


@app.route('/index')
def index():
    """The function that is called when directing to the /index part of the webpage

    This is the main homescreen of the webpage and will be refreshed every minute
    This procedure checks if an action has been carried out on the webpage
    This procedure also sets the values for events, news, covid data and images
    :return: The template for the webpage
    """
    # Runs the scheduler making sure not to stop other commands being carried out
    scheduler = get_scheduler()
    if not scheduler.empty():
        scheduler.run(blocking=False)
    # Retrieves covid values and news articles
    local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths = get_covid_values()
    articles = get_news_articles()
    event_to_remove = request.args.get('update_item')
    news_to_remove = request.args.get('notif')
    if event_to_remove:
        remove_event(event_to_remove)
        articles = get_news_articles()
    # Checks if there is news to be removed
    if news_to_remove:
        # Will remove news from being searched for and update the display
        update_removed_news(news_to_remove)
        remove_news_from_home()
    label_name = request.args.get('two')
    # Checks if a scheduled event has been added
    if label_name:
        # Checks if event is already in scheduler
        if event_exists(label_name):
            logging.info("Event already present")
        else:
            # Checks if a time has been added along with an article
            scheduler_time = request.args.get('update')
            if scheduler_time:
                # Receives information on what is to be updated
                repeat = request.args.get('repeat')
                data_to_update = request.args.get('covid-data')
                news_to_update = request.args.get('news')
                add_update(repeat, data_to_update, news_to_update, label_name, scheduler_time)
            else:
                logging.info("No time provided")
    # Assigns values to the parts of the application
    return render_template('index.html', title='Daily Update', news_articles=articles,
                           updates=scheduled_events, image=image_name,
                           local_7day_infections=local_week_figs,
                           national_7day_infections=nation_week_figs,
                           hospital_cases=nation_hospital_figs, deaths_total=nation_deaths,
                           location=location, nation_location=nation_location)


if __name__ == '__main__':
    app.run()
