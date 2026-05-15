# 🤖 AI Review Classification & Management System

A beginner-friendly cloud computing mini-project that uses **Natural Language Processing (NLP)** to automatically analyze product reviews — detecting sentiment and product category — and provides an **admin dashboard** to manage review resolution status.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Installation & Setup (Windows / VS Code)](#installation--setup-windows--vs-code)
6. [How to Run the Project](#how-to-run-the-project)
7. [How SQLite Works](#how-sqlite-works)
8. [How Sentiment Analysis Works](#how-sentiment-analysis-works)
9. [How Category Classification Works](#how-category-classification-works)
10. [AWS EC2 Deployment Guide](#aws-ec2-deployment-guide)
11. [Screenshots](#screenshots)
12. [Future Improvements](#future-improvements)

---

## 🌟 Project Overview

This system allows users to submit product reviews through a web interface. The backend automatically:

- **Detects sentiment** (Positive / Negative / Neutral) using TextBlob NLP
- **Detects product category** (Phone, Laptop, Chair, etc.) using keyword matching
- **Stores all reviews** in a local SQLite database
- **Provides an Admin Dashboard** where an operator can view, filter, search, and update the status of all reviews

This project is suitable as a **cloud computing mini-project** and can be deployed on **AWS EC2** with minimal configuration.

---

## ✅ Features

### User Review Page
- Clean text input form for submitting reviews
- Example review buttons for quick testing
- Real-time character counter
- Instant analysis result shown after submission
- Flash messages for success/error feedback

### Sentiment Analysis
- Uses **TextBlob** polarity score
- Three classes: Positive, Negative, Neutral

### Product Category Detection
- Keyword-based matching for 10 product categories
- Fallback to "Other" if no category found

### Admin Dashboard
- View all submitted reviews in a table
- Summary stats: total, positive, negative, unresolved counts
- Filter by: Sentiment, Category, Status
- Search by keyword in review text
- Update status inline: Unresolved → Under Process → Resolved
- Delete reviews
- Auto-submit filters on dropdown change

---

## 🛠️ Technologies Used

| Layer      | Technology              | Purpose                          |
|------------|-------------------------|----------------------------------|
| Backend    | Flask 3.x               | Web framework                    |
| Database   | SQLite + SQLAlchemy ORM | Data storage                     |
| NLP        | TextBlob                | Sentiment analysis               |
| ML/Data    | scikit-learn, pandas    | ML utilities (expandable)        |
| NLP Extras | nltk, joblib            | Text processing support          |
| Frontend   | Bootstrap 5             | Responsive UI                    |
| Frontend   | Vanilla CSS + JS        | Custom styling & interactivity   |

---

## 📁 Project Structure

```
project/
│
├── app.py                  ← Main Flask application (all routes)
├── requirements.txt        ← Python dependencies
├── reviews.db              ← SQLite database (auto-created on first run)
├── README.md               ← This file
│
├── models/
│   ├── __init__.py
│   └── database.py         ← SQLAlchemy Review model + db init
│
├── utils/
│   ├── __init__.py
│   ├── sentiment.py        ← TextBlob sentiment analysis function
│   └── category.py         ← Keyword-based category detection function
│
├── templates/
│   ├── index.html          ← User review submission page
│   └── dashboard.html      ← Admin dashboard page
│
└── static/
    ├── css/
    │   └── style.css       ← Custom CSS (modern design)
    └── js/
        └── main.js         ← Client-side JS (form validation, UX)
```

---

## 🖥️ Installation & Setup (Windows / VS Code)

### Prerequisites
- Python 3.9+ installed ([python.org](https://python.org))
- VS Code installed ([code.visualstudio.com](https://code.visualstudio.com))
- Git (optional)

### Step 1 — Open the Project in VS Code

```
File → Open Folder → Select your project folder
```

### Step 2 — Open the Integrated Terminal in VS Code

```
Terminal → New Terminal   (or Ctrl + `)
```

### Step 3 — Create a Virtual Environment

```powershell
python -m venv venv
```

This creates an isolated Python environment inside a `venv/` folder.

### Step 4 — Activate the Virtual Environment

```powershell
venv\Scripts\activate
```

You should see `(venv)` at the start of the terminal prompt.

### Step 5 — Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 6 — Download TextBlob Language Data

TextBlob needs extra data for sentiment analysis:

```powershell
python -m textblob.download_corpora
```

> If that doesn't work, run: `python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"`

---

## ▶️ How to Run the Project

```powershell
python app.py
```

You should see:

```
[DB] Database initialized — tables created if not present.
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

Open your browser and go to:

- **User Review Page:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Admin Dashboard:** [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)

To stop the server: press `Ctrl + C` in the terminal.

---

## 🗄️ How SQLite Works

SQLite is a lightweight, file-based database — perfect for development and small projects.

- The database file `reviews.db` is **automatically created** the first time you run `app.py`
- No separate database server is needed
- The database stores all reviews in a table called `reviews`

**Table columns:**

| Column       | Type     | Description                              |
|--------------|----------|------------------------------------------|
| id           | Integer  | Auto-incremented unique ID               |
| review_text  | Text     | The raw review entered by the user       |
| sentiment    | String   | Positive / Negative / Neutral            |
| category     | String   | Detected product category                |
| status       | String   | Unresolved / Under Process / Resolved    |
| created_at   | DateTime | Timestamp when the review was submitted  |

**SQLAlchemy ORM** (Object Relational Mapper) allows us to work with the database using Python objects instead of raw SQL queries. For example:

```python
# Saving a review
new_review = Review(review_text="Great phone!", sentiment="Positive", ...)
db.session.add(new_review)
db.session.commit()

# Fetching reviews
reviews = Review.query.filter_by(sentiment="Positive").all()
```

---

## 😊 How Sentiment Analysis Works

**Library used:** [TextBlob](https://textblob.readthedocs.io)

TextBlob is a Python NLP library. It analyzes text and returns a **polarity score** between -1.0 and +1.0:

| Polarity Range | Meaning  | Our Label  |
|---------------|---------|-----------|
| > 0.1         | Positive | ✅ Positive |
| < -0.1        | Negative | ❌ Negative |
| Between       | Neutral  | ➖ Neutral  |

**Code example (`utils/sentiment.py`):**

```python
from textblob import TextBlob

def analyze_sentiment(review_text):
    blob = TextBlob(review_text)
    polarity = blob.sentiment.polarity  # -1.0 to +1.0

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
```

**Examples:**
- "The phone is amazing!" → polarity ≈ 0.8 → **Positive**
- "The chair was broken and terrible" → polarity ≈ -0.7 → **Negative**
- "The laptop battery is average" → polarity ≈ 0.0 → **Neutral**

---

## 🏷️ How Category Classification Works

**Method:** Simple keyword matching (no ML model needed)

A Python dictionary maps each category to a list of keywords:

```python
CATEGORY_KEYWORDS = {
    "Phone":      ["phone", "smartphone", "mobile", "iphone"],
    "Laptop":     ["laptop", "notebook", "macbook"],
    "Chair":      ["chair", "seat", "stool"],
    # ... etc
}
```

The review is converted to **lowercase**, then scanned for each keyword. The first match wins.

**Examples:**
- "My phone screen cracked" → finds "phone" → **Phone**
- "The laptop is slow" → finds "laptop" → **Laptop**
- "It arrived broken" → no keyword found → **Other**

This approach is simple, fast, and easy to extend by adding more keywords.

---

## ☁️ AWS EC2 Deployment Guide

### Step 1 — Launch an EC2 Instance

1. Log in to [AWS Console](https://console.aws.amazon.com)
2. Go to **EC2 → Instances → Launch Instance**
3. Choose **Ubuntu Server 22.04 LTS (Free Tier)**
4. Instance type: **t2.micro** (Free Tier)
5. Create or select a key pair (`.pem` file) — save it safely
6. Under **Security Group**, add a rule:
   - Type: Custom TCP
   - Port: `5000`
   - Source: `0.0.0.0/0` (allows public access)
7. Click **Launch Instance**

### Step 2 — Connect to Your EC2 Instance (SSH)

On Windows, use PowerShell or Git Bash:

```bash
ssh -i "your-key.pem" ubuntu@<your-ec2-public-ip>
```

> Replace `your-key.pem` with your key file path and `<your-ec2-public-ip>` with your EC2 public IP.

On first connect, type `yes` to accept the fingerprint.

### Step 3 — Install Python on EC2

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### Step 4 — Upload Your Project to EC2

**Option A — Using SCP (from your Windows terminal):**

```bash
scp -i "your-key.pem" -r "C:/path/to/project" ubuntu@<ec2-ip>:~/ai-review-system
```

**Option B — Using Git:**

```bash
git clone https://github.com/yourusername/ai-review-system.git
cd ai-review-system
```

### Step 5 — Create Virtual Environment & Install Requirements

```bash
cd ~/ai-review-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m textblob.download_corpora
```

### Step 6 — Run the Flask App

```bash
python app.py
```

### Step 7 — Access the App in Your Browser

Open your browser and go to:

```
http://<your-ec2-public-ip>:5000
```

> Make sure port 5000 is open in your EC2 Security Group (Step 1).

### Step 8 (Optional) — Keep the App Running in Background

```bash
nohup python app.py > output.log 2>&1 &
```

This keeps the app running even after you close the SSH session.

### Step 9 (Optional) — Use a Process Manager (PM2 or Gunicorn)

For production, run with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📸 Screenshots

> *(Add screenshots here after running the application)*

| Page             | Description                              |
|------------------|------------------------------------------|
| Review Page      | User submits a review, sees result       |
| Analysis Result  | Sentiment and category displayed         |
| Admin Dashboard  | All reviews with stats and filter bar    |
| Status Update    | Operator changes review status inline    |

---

## 🚀 Future Improvements

1. **User Authentication** — Add login for admin dashboard
2. **Advanced ML Model** — Replace keyword matching with a trained TF-IDF or BERT classifier
3. **Email Notifications** — Notify admins when new negative reviews arrive
4. **Charts & Analytics** — Add Plotly/Chart.js charts on the dashboard
5. **Pagination** — Handle large numbers of reviews efficiently
6. **Export to CSV** — Let admin download review data
7. **Multi-language Support** — Detect sentiment in languages other than English
8. **REST API** — Expose endpoints for mobile/other frontends
9. **PostgreSQL** — Upgrade from SQLite to PostgreSQL for production
10. **Docker** — Containerize for easier deployment

---

## 📄 License

This project is for educational purposes. Free to use and modify.

---

> Built with ❤️ using Flask · TextBlob · SQLAlchemy · Bootstrap 5
