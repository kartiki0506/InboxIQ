# 📧 InboxIQ – Smart Email Classifier

InboxIQ is a Flask-based web application that connects to Gmail and intelligently classifies emails into categories such as Internship, Events, Academic, Spam, and General. It also allows users to set reminders for important emails.

---

## 🚀 Features

* 📥 Fetch emails using Gmail API
* 🧠 Smart classification using email subject + body
* 📊 Dashboard with category-based filtering
* ⏰ Reminder system with custom time (HH/MM/AM-PM)
* 🔔 Desktop notifications for reminders

---

## 🛠️ Technologies Used

* Python
* Flask
* Gmail API
* HTML & CSS
* Plyer (for notifications)

---

## 📁 Project Structure

```
InboxIQ/
│
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── cover.html
│   ├── dashboard.html
│   └── reminder.html
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/InboxIQ.git
cd InboxIQ
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Get Your Own Gmail API Credentials

⚠️ Important:
`credentials.json` is NOT included for security reasons.
You must create your own.

---

### Steps to Create Credentials

1. Go to: https://console.cloud.google.com/

2. Click **Select Project → New Project**

3. Enter a project name and create it

4. Go to **APIs & Services → Library**

5. Search for **Gmail API** and enable it

6. Go to **APIs & Services → Credentials**

7. Click **Create Credentials → OAuth Client ID**

8. If asked:

   * Configure OAuth Consent Screen
   * Choose **External**
   * Fill basic details

9. Then:

   * Application type → Desktop App
   * Click Create

10. Download the JSON file

---

### Place the file

Rename the downloaded file to:

```
credentials.json
```

Place it in the root project folder.

---

### 4. Run the Application

```
python app.py
```

---

### 5. Open in Browser

```
http://127.0.0.1:5000/
```

---

## 🔐 Security Note

* `credentials.json` is excluded using `.gitignore`
* Each user must generate their own credentials
* This ensures secure API usage

---

## 🎯 Future Improvements

* Machine Learning-based classification
* Email analytics dashboard
* Search functionality
* Dark mode UI
* Calendar integration

---

## 👩‍💻 Author

Kartiki Sinha

---
