from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
import os

from email_service import send_email


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(send_email, 'cron', day_of_week='tue', hour=20, minute=15)  # server time is 2 hours behind Prague time
    scheduler.start()


@app.route("/send_email", methods=['GET'])
def send_events_email():

    send_email()

    return "Email has been sent!"


if __name__ == "__main__":
    app.run(use_reloader=False)
