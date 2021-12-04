"""
This is the main module which will deal with flask and the flow of the program
"""
import logging
from flask import Flask
from flask import render_template
from flask import request
import covid_data_handler
from covid_data_handler import update_covid_data
from covid_news_handling import update_news
from covid_news_handling import update_removed_news
from covid_news_handling import schedule_news_updates
from shared_data import get_covid_values
from shared_data import get_scheduler
from shared_data import set_news_articles
from shared_data import get_news_articles
from shared_data import set_scheduled_events
from decode_config import decode_config

# error with internal server error when event is scheduled and run
# Default values are received for when the website is first opened
# Scheduler and app are also created here
articles = update_news()
set_news_articles(articles)
scheduled_events = []
set_scheduled_events(scheduled_events)
app = Flask(__name__)
location, _, nation_location, _, _, image_name = decode_config()

if image_name == "":
    image_name = "covid_image.jpeg"

if location == "":
    location = "Exeter"

update_covid_data()


def event_update(title, content, to_update, repeat):
    """
    This procedure will add an event to the scheduled_events array
    This will be added to the left hand side of the webpage
    :param repeat: Whether the event is to be repeated
    :param to_update: What is to be updated
    :param title: Title of the event
    :param content: Content displayed under the title
    """
    scheduled_events.append({'title': title, 'content': content,
                             'to_update': to_update, 'repeat': repeat})
    set_scheduled_events(scheduled_events)


def remove_event(title):
    """
    Will remove event with the title provided from scheduled_events
    :param title: the title of the event to be removed
    """
    for event in scheduled_events:
        if event['title'] == title:
            scheduled_events.remove(event)
            break
    logging.warning("No event found with that name")


def event_exists(title):
    """
    Will cycle through events with the title provided from scheduled_events
    :param title: the title of the event to be removed
    :return True if event present otherwise False
    """
    present = False
    for event in scheduled_events:
        if event['title'] == title:
            present = True
    return present


def remove_news_from_home():
    """
    Changes articles when news has been removed so that the display can be updated
    """
    global articles
    articles = update_news()


def add_update(repeat, data_to_update, news_to_update, label_name, scheduler_time):
    """
    Will update both schedulers if both news and covid data are to be updated
    Will also deal if only one is to updated or neither
    :param repeat: Whether the event is to be repeated every 24 hours
    :param data_to_update: Whether the covid data is to be update
    :param news_to_update: Whether the news is to be update
    :param label_name: The name of the event to be added
    :param scheduler_time: The time the event is to be added
    """
    if data_to_update and news_to_update:
        event_update(label_name, scheduler_time, 'both', repeat)
        covid_data_handler.schedule_covid_updates(scheduler_time, label_name)
        schedule_news_updates(scheduler_time, label_name)
    elif data_to_update:
        event_update(label_name, scheduler_time, 'covid', repeat)
        covid_data_handler.schedule_covid_updates(scheduler_time, label_name)
    elif news_to_update:
        event_update(label_name, scheduler_time, 'news', repeat)
        schedule_news_updates(scheduler_time, label_name)
    else:
        logging.info('Nothing provided to update')


@app.route('/index')
def index():
    """
    The function that is called when directing to the /index part of the webpage
    This is the main homescreen of the webpage and will be refreshed every minute
    This procedure checks if an action has been carried out on the webpage
    This procedure also sets the values for events, news, covid data and images
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
            print("Error: Event already present")
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
