# 🏨 Smart_stay — Hotel Package Suggester

An AI-powered hotel package recommender that analyzes past customer feedback and visit history to suggest personalized packages using Google's Gemini API.  
Built with **Streamlit** (frontend) and **Flask** (backend).

How to Run (Windows Only)

1. Clone the Repository
git clone https://github.com/IconicShivani1206/Smart_stay.git
cd Smart_stay

2. Create and Activate Virtual Environment (Windows)
python -m venv venv
venv\Scripts\activate

3. Install Required Packages
pip install -r requirements.txt

4. Start Backend (Flask)
cd backend
python app.py

5. Start Frontend (Streamlit)
cd frontend
streamlit run hotel_ui.py