import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

msg = MIMEText("This is a test email from BookTable integration.")
msg["Subject"] = "Test Email"
msg["From"] = os.getenv("FROM_EMAIL")
msg["To"] = "priya.jadhav047@gmail.com"

with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
    server.starttls()
    server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
    server.send_message(msg)

print("Test email sent!")