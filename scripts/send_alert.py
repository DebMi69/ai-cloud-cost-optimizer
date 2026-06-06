import smtplib
from email.mime.text import MIMEText

sender_email = "rohanchicken64@gmail.com"
app_password = "pqxhgpjrzmzfqlxw"

receiver_email = "mitramar68@gmail.com"

message = MIMEText(
    "High CPU Utilization Detected in Azure VM"
)

message["Subject"] = "Azure Alert"
message["From"] = sender_email
message["To"] = receiver_email

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(message)

print("Alert sent successfully")