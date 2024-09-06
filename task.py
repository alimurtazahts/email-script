import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Fetch email details from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Read tasks from the file
def read_tasks_from_file(file_path):
    tasks = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                day, task = line.split(':', 1)
                tasks[day.strip()] = task.strip()
    return tasks

# Get tasks from the tasks.txt file
tasks = read_tasks_from_file('tasks.txt')

def get_today_task():
    """Get the task for today based on the day of the week."""
    today = datetime.now().strftime("%A")
    return tasks.get(today, "No task assigned for today.")

def send_email(task):
    """Send an email with the given task."""
    # Email setup
    email_sender = EMAIL_ADDRESS
    email_password = EMAIL_PASSWORD
    email_receiver = RECIPIENT_EMAIL
    
    subject = "Your Daily Task"
    body = f"This is your task for today:\n\n{task}"

    # Create email
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def daily_task():
    """Get today's task and send it via email."""
    task = get_today_task()
    send_email(task)

# Schedule the task to run daily at a specific time (e.g., 5:37 PM)
schedule.every().day.at("17:51").do(daily_task)

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait for 60 seconds before checking the schedule again
