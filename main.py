from flask import Flask
from flask import render_template
from flask import request
from covid_news_handling import update_news
import sched
import time


app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
articles = update_news()


def news_update():
    global articles
    articles = update_news()


def schedule_add_news():
    event = s.enter(15, 1, news_update())


@app.route('/index')
def index():
    s.run(blocking=False)
    label_name = request.args.get('two')
    if label_name:
        # check scheduler_time exists
        scheduler_time = request.arg.get('update')
        schedule_add_news()
    return render_template('index.html', title='Daily Update', news_articles=articles)


if __name__ == '__main__':
    app.run()
