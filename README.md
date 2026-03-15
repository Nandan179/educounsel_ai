# EduCounsel AI 🎓

EduCounsel AI is an intelligent, full-stack educational counseling platform built to help prospective students find the best universities globally tailored to their desired course, location, and annual budget. 

It features an **AI Chatbot Counselor** powered by a Machine Learning prediction engine to recommend, score, and rank nearly 1,000 top universities dynamically.

## 🚀 Features

*   **AI-Powered Recommendations:** Utilizes a custom-trained Random Forest model (`scikit-learn`) to calculate a personalized "Suitability Score" for each university.
*   **Interactive Chatbot Counselor:** A step-by-step intuitive UI that acts as a virtual counselor, gracefully collecting user preferences (Course, Country, Budget).
*   **Massive Offline Dataset:** Pre-loaded with over 950 legitimate universities and 8,500+ courses across the US, UK, Japan, Singapore, India, Germany, and more.
*   **Live Web Fallback API:** If a user searches for a highly obscure course not in our offline database, the system automatically runs a live internet search via the open **Hipolabs API** to construct dynamic university recommendations on the fly.
*   **University Comparison Tool:** A dynamic dashboard to select and strictly compare two institutions side-by-side (rankings, fees, accreditation).
*   **Glassmorphism Aesthetic:** A highly modern, responsive frontend unified through Django templating, featuring rich hover states, dynamic progress bars, and premium UI design.

## 🛠️ Architecture

*   **Framework:** Django (Python) using Model-View-Template (MVT) architecture.
*   **Database:** SQLite (managed via Django ORM).
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap Icons, Google 'Inter' Font.
*   **Machine Learning:** Pandas, Scikit-Learn (`RandomForestRegressor`).

## ⚙️ How It Works (The ML Pipeline)
1.  **Data Ingestion:** Scripts parse large CSV datasets (Universities, Courses, Policies) directly into the relational SQLite database.
2.  **Training Phase (`train_model.py`):** The model merges the data and uses `LabelEncoder` to convert categorical text (like 'course name' and 'country') into numbers. It trains a `RandomForestRegressor` to predict a suitability score based on ranking, fees, and location logic.
3.  **Real-Time Prediction Context:** When a user chats with the bot, the backend (`views.py`) captures their state, queries the SQLite database for matches, and feeds those matches through the loaded `.pkl` model to generate an AI match score before rendering the UI cards.

## 📥 Setup & Installation

If you would like to run this application locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Nandan179/educounsel_ai.git
    cd educounsel_ai
    ```
2.  **Create a Virtual Environment & Install Dependencies:**
    *(Ensure you have Python 3 installed)*
    ```bash
    python -m pip install django pandas scikit-learn requests beautifulsoup4
    ```
3.  **Initialize the Database:**
    ```bash
    cd config
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Import the University Data:**
    ```bash
    python manage.py import_world_data
    ```
5.  **Train the Machine Learning Model:**
    Return to the root directory and run the training pipeline to generate `rf_model.pkl`:
    ```bash
    cd ..
    python train_model.py
    ```
6.  **Run the Server:**
    ```bash
    cd config
    python manage.py runserver
    ```
7.  Visit `http://127.0.0.1:8000/chat` to start!

## 🤝 Project Background
Developed as a capstone review project to showcase the integration of monolithic web frameworks (Django) with offline machine learning models (Random Forest) and live third-party internet APIs.
