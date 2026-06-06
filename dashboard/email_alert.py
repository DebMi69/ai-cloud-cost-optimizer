import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"


def send_alert(subject, body):

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.send_message(message)

    print("Alert sent")