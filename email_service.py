import smtplib
from email.message import EmailMessage
from jinja2 import Template
from calendar_service import get_events

EMAIL_ADDRESS = 'jantheprogrammer@gmail.com'
EMAIL_SERVICE_PSW = 'vswcfsiwxhvwpcnb'  # psw from google


def send_email():
    msg = EmailMessage()
    msg['Subject'] = 'Up coming events!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.set_content('This is a plain text email.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_SERVICE_PSW)
        # get events from google calendar
        events = get_events()
        # use jinja2 template for creating the email layout
        prepare_email(msg, events)
        smtp.send_message(msg)


def prepare_email(msg, events):
    # \ the backslash cancels new line
    data = """\
    <!DOCTYPE html>
    <html>      
        <body>
                
            {% if events %}
                <h1 style='color: #6a0f0f;'>
                    Upcoming events!
                </h1>
                <ul>
                    {% for event in events %}
                    
                        <li style='padding: 4px 8px;
                            list-style: none;
                            color: #003303;
                            text-align: initial;
                            font-size: 18px;
                            border-bottom: 2px solid darkred;'>
                            
                             {{ event.date }} {{ event.description }} <i> {{ event.summary }} </i>
                        </li>
                             
                    {% endfor %}
                </ul>
            {% else %}
                <h1 style='color: #6a0f0f;'>
                    No upcoming events!
                </h1>
            {% endif %}
            
        </body>
    </html>
    """

    template = Template(data)
    email = template.render(events=events)
    msg.add_alternative(email, subtype='html')
