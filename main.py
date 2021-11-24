from flask import Flask
from flask import render_template
from flask import request
from covid_news_handling import update_news
import sched
import time


app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
articles = update_news()


def scheduled_news_update():
    global articles
    articles = update_news()


@app.route('/index')
def index():
    return render_template('index.html', title='Daily Update', news_articles=articles)


if __name__ == '__main__':
    app.run()
