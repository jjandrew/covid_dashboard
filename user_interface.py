"""
This is the main module which will deal with flask and the flow of the program
"""
import sched
import time
from flask import Flask
from flask import render_template
from flask import request
from decode_config import decode_config
from covid_news_handling import update_news
from covid_data_handler import process_covid_API
from covid_data_handler import covid_API_request


# error with internal server error when event is scheduled and run
# Default values are received for when the website is first opened
# Scheduler and app are also created here
articles = update_news()
scheduled_events = []
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
location, location_type, _, _, image_name = decode_config()
week_figs, hospital_figs, total_deaths = 0, 0, 0


if image_name == "":
    image_name = "covid_image.jpeg"


if location == "" or location_type == "":
    week_figs, hospital_figs, total_deaths = process_covid_API(covid_API_request())
else:
    week_figs, hospital_figs, total_deaths = process_covid_API(covid_API_request(location,
                                                                                 location_type))


def news_update():
    """
    Procedure for updating the global variable articles
    This will be called by the scheduler
    """
    global articles
    articles = update_news()


def covid_data_update():
    """
    Procedure for updating the global variable articles
    This will be called by the scheduler
    """
    global week_figs, hospital_figs, total_deaths
    week_figs, hospital_figs, total_deaths = process_covid_API(covid_API_request())


def event_update(title, content):
    """
    This procedure will add an event to the scheduled_events array
    This will be added to the left hand side of the webpage
    :param title: Title of the event
    :param content: Content displayed under the title
    """
    scheduled_events.append({'title': title, 'content': content})


# These need to be moved into covid_news_handling and covid_data_handler
def schedule_add_news(delay=15, repeat=False):
    """
    Adds an event to the scheduler to update the news
    :param repeat: Checks if the scheduled event is to be repeated, default set to False
    :param delay: Delay for the scheduler
    """
    event = s.enter(delay, 1, news_update())
    print(event, repeat)


def schedule_update_data(delay=15, repeat=False):
    """
    Adds an event to the scheduler to update covid data
    :param repeat: Checks if the scheduled event is to be repeated, default set to False
    :param delay: Delay for the scheduler
    """
    event = s.enter(delay, 1, news_update())
    print(event, repeat)


@app.route('/index')
def index():
    """
    The function that is called when directing to the /index part of the webpage
    This is the main homescreen of the webpage and will be refreshed every minute
    This procedure checks if an action has been carried out on the webpage
    This procedure also sets the values for events, news, covid data and images
    """
    # Runs the scheduler making sure not to stop other commands being carried out
    if s:
        s.run(blocking=False)
    label_name = request.args.get('two')
    # Checks if a scheduled event has been added
    if label_name:
        # Checks if a time has been added along with an article
        scheduler_time = request.args.get('update')
        if scheduler_time:
            # Receives information on what is to be updated
            repeat = request.args.get('repeat')
            data_to_update = request.args.get('covid-data')
            news_to_update = request.args.get('news')
            # Will update both schedulers if both news and covid data are to be updated
            # Will also deal if only one is to updated or neither
            if data_to_update and news_to_update:
                event_update(label_name, scheduler_time)
                schedule_update_data()
                schedule_add_news()
            elif data_to_update:
                event_update(label_name, scheduler_time)
                schedule_update_data()
            elif news_to_update:
                event_update(label_name, scheduler_time)
                schedule_add_news()
            else:
                print('Nothing to update')
        else:
            print("No time provided")
    # Assigns values to the parts of the application
    return render_template('index.html', title='Daily Update', news_articles=articles,
                           updates=scheduled_events, image=image_name,
                           national_7day_infections=week_figs, hospital_cases=hospital_figs,
                           deaths_total=total_deaths)


if __name__ == '__main__':
    app.run()
