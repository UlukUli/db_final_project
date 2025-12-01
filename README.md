# 📌 Hotel Booking — Final Database Project

This repository contains a team project for the **Hotel Booking Database**.  
The project includes database design, SQL analytics, and an AI-powered SQL agent.

---

## 🧩 Team Roles
- **Database Architect** — ERD, schema design, normalization  
- **Data Analyst** — insights, visualizations, reporting  
- **SQL Developer** — queries, views, stored procedures  
- **AI Engineer** — AI SQL agent for natural-language questions

---

## 🗂 Project Structure

```
DB_Final_Project/
│── architect/           # ERD & schema (from Architect)
│── analyst/             # analysis, charts, insights
│── sql_developer/       # SQL scripts
│── ai_agent/            # AI notebook + helper scripts
│── data/                # dataset
│── database/            # MySQL dump (schema + data)
│── docs/                # documentation
│── presentation/        # project slides
│── requirements.txt
│── README.md
```

---

## ⚙️ Technologies Used
- **MySQL**  
- **Python (Jupyter Notebook)**  
- **SQLAlchemy + PyMySQL**  
- **Pandas, NumPy, Seaborn, Matplotlib**  
- **Google Gemini API** (AI → SQL)

---

## 💡 AI SQL Agent
The AI module can:
- Convert natural language into SQL  
- Execute SQL queries on MySQL  
- Return results as tables  
- Generate charts and simple insights  

Located in:  
```
/ai_agent/ai_agent.ipynb
```

---

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env` file (MySQL + Gemini API keys)  
3. Run the notebook:
   ```
   jupyter notebook
   ```

---

## 📄 License
For educational purposes only.
