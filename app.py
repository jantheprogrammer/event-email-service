from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS

from email_service import send_email

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(send_email, 'cron', day_of_week='mon', hour=6)  # heroku server time is 2 hours behind Prague time
scheduler.start()


@app.route("/send_email", methods=['GET'])
def send_events_email():
    send_email()

    return "Email has been sent!"


if __name__ == "__main__":
    app.run()
