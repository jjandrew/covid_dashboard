from flask import Flask
from flask import render_template
from flask import request
from covid_news_handling import update_news
from covid_data_handler import process_covid_API
from covid_data_handler import covid_API_request
import sched
import time

# error with internal server error when event is scheduled and run
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
articles = update_news()
scheduled_events = [{'title': 'TEST', 'content': 'Content'}]
week_figs, hospital_figs, total_deaths = process_covid_API(covid_API_request())


def news_update():
    global articles
    articles = update_news()


def event_update(title, time):
    scheduled_events.append({'title': title, 'content': time})


def schedule_add_news(time=15):
    event = s.enter(time, 1, news_update())


def schedule_update_data(time=15):
    event = s.enter(time, 1, news_update())



@app.route('/index')
def index():
    if s:
        s.run(blocking=False)
    label_name = request.args.get('two')
    if label_name:
        # check scheduler_time exists
        scheduler_time = request.args.get('update')
        if scheduler_time:
            repeat = request.args.get('repeat')
            update_data = request.args.get('covid-data')
            update_news = request.args.get('news')
            if update_data and update_news:
                event_update(label_name, scheduler_time)
                schedule_update_data()
                schedule_add_news()
            elif update_data:
                event_update(label_name, scheduler_time)
                schedule_update_data()
            elif update_news:
                event_update(label_name, scheduler_time)
                schedule_add_news()
            else:
                print('Nothing to update')
        else:
            print("No time provided")
    return render_template('index.html', title='Daily Update', news_articles=articles, updates=scheduled_events, image='covid_image.jpeg', national_7day_infections=week_figs, hospital_cases=hospital_figs, deaths_total=total_deaths)


if __name__ == '__main__':
    app.run()
