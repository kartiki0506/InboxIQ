# ==============================
# 📧 InboxIQ - Email Classifier
# ==============================

# -------- IMPORTS --------
from flask import Flask, render_template, request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from plyer import notification
import threading
import time
import re

# -------- APP INIT --------
app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# -------- GLOBAL SERVICE (avoid login again & again) --------
service = None


# ---------------- AUTH ----------------
def authenticate():
    global service

    if service is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        service = build('gmail', 'v1', credentials=creds)

    return service


# ---------------- CLASSIFIER ----------------
def classify_email(text):
    text = text.lower()

    if any(word in text for word in ["internship", "apply", "career", "job"]):
        return "Internship"

    elif any(word in text for word in ["event", "workshop", "seminar", "webinar"]):
        return "Event"

    elif any(word in text for word in ["gate", "exam", "result", "program", "course"]):
        return "Academic"

    elif any(word in text for word in ["win", "offer", "discount", "sale"]):
        return "Spam"

    else:
        return "General"


# ---------------- FETCH EMAILS ----------------
def get_emails():
    service = authenticate()

    results = service.users().messages().list(
        userId='me', maxResults=15).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        txt = service.users().messages().get(
            userId='me', id=msg['id']).execute()

        payload = txt['payload']
        headers = payload['headers']

        subject, sender, body = "", "", ""

        # Extract subject & sender
        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']

        # Extract body
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        import base64
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        else:
            data = payload['body'].get('data')
            if data:
                import base64
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        # Combine subject + body for better classification
        full_text = subject + " " + body

        category = classify_email(full_text)

        emails.append({
            "subject": subject,
            "sender": sender,
            "category": category
        })

    return emails
    service = authenticate()

    results = service.users().messages().list(
        userId='me', maxResults=15).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        txt = service.users().messages().get(
            userId='me', id=msg['id']).execute()

        headers = txt['payload']['headers']

        subject, sender = "", ""

        for h in headers:
            if h['name'] == 'Subject':
                subject = h['value']
            if h['name'] == 'From':
                sender = h['value']

        category = classify_email(subject)

        emails.append({
            "subject": subject,
            "sender": sender,
            "category": category
        })

    return emails


# ---------------- REMINDER THREAD ----------------
def reminder_thread(email, seconds):
    time.sleep(seconds)

    notification.notify(
        title="Reminder 🔔",
        message=email,
        timeout=10
    )


# ---------------- LOAD SAVED REMINDERS ----------------
def load_reminders():
    try:
        with open("reminders.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            email_text, time_sec = line.strip().split("|")
            time_sec = int(time_sec)

            threading.Thread(
                target=reminder_thread,
                args=(email_text, time_sec)
            ).start()

    except:
        pass


# ---------------- ROUTES ----------------

# Cover Page
@app.route("/")
def cover():
    return render_template("cover.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():
    emails = get_emails()
    filter_type = request.args.get("filter")

    if filter_type:
        emails = [e for e in emails if e['category'] == filter_type]

    return render_template("dashboard.html", emails=emails)


# Reminder Page
@app.route("/reminder", methods=["GET", "POST"])
def reminder():
    emails = get_emails()

    if request.method == "POST":
        email_text = request.form["email"]
        from datetime import datetime

        hour = int(request.form["hour"])
        minute = int(request.form["minute"])
        ampm = request.form["ampm"]

        # Convert to 24-hour format
        if ampm == "PM" and hour != 12:
            hour += 12
        if ampm == "AM" and hour == 12:
            hour = 0

        now = datetime.now()
        target_time = now.replace(hour=hour, minute=minute, second=0)

        # If time already passed → set for next day
        if target_time < now:
            target_time = target_time.replace(day=now.day + 1)

        time_sec = int((target_time - now).total_seconds())

        # Save reminder
        with open("reminders.txt", "a") as f:
            f.write(f"{email_text}|{time_sec}\n")

        # Start thread
        threading.Thread(
            target=reminder_thread,
            args=(email_text, time_sec)
        ).start()

        return "✅ Reminder Set Successfully!"

    return render_template("reminder.html", emails=emails)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    load_reminders()   # load saved reminders
    app.run(debug=True)
