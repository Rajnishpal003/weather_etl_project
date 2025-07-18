
# 🌤️ Real-Time Weather ETL Dashboard

## 🚀 Project Overview

This project demonstrates:

- 🔄 ETL (Extract, Transform, Load) pipeline in Python
- 🧠 Use of APIs (`requests` with `.env` for security)
- 🗃️ PostgreSQL integration for storage
- 📈 Real-time dashboard using Streamlit
- 🧼 Modern practices with SQLAlchemy and `.gitignore`
- 📦 Deployment-ready with `requirements.txt`

---

## 🔧 Tech Stack

| Layer         | Tech                     |
|---------------|--------------------------|
| ETL Script     | Python, `requests`, `dotenv` |
| Database       | PostgreSQL              |
| ORM            | SQLAlchemy              |
| Visualization  | Streamlit               |
| Deployment     | Streamlit Cloud         |

---

## 📁 Project Structure

weather\_etl\_project/
├── weather\_etl.py         ← Python ETL script (API → PostgreSQL)
├── dashboard.py           ← Streamlit UI app
├── .env                   ← API key (ignored from Git)
├── requirements.txt       ← All dependencies
├── .gitignore             ← Clean repo (no secrets or cache)
└── README.md              ← This file!

---

## 📥 Setup Instructions

### ✅ Clone Repo

git clone https://github.com/yourusername/weather-etl-dashboard.git
cd weather-etl-dashboard

### ✅ Create Virtual Environment

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### ✅ Set Up Environment

Create a `.env` file with your OpenWeatherMap API key:

API_KEY=your_actual_api_key

---

## 🧪 Run ETL Script Manually

python3 weather_etl.py

---

## 🌐 Run Dashboard

streamlit run dashboard.py

* View the latest weather data
* Fetch new updates
* See charts for temperature & humidity trends
* Clean modern UI with auto-refresh!


## 💾 PostgreSQL Table Schema

```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    description VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

## 👨‍💻 Author

**Rajnish Pal Singh**
🔗 [LinkedIn](https://www.linkedin.com/in/rajnish-pal-singh/)
📫 [rajnishpalsingh@gmail.com](mailto:rajnishpalsingh006@gmail.com)

---

## 📃 License

MIT – use this project freely for personal or academic use.




