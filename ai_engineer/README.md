# AI Text-to-SQL Agent (Hotel Booking Project)

This folder contains the AI integration part of our **Hotel Booking Analytics System**.
The goal of this component is to enable **natural-language questions** that are
automatically translated into **SQL queries** and executed against our MySQL database.

## Files

- `ai_agent_clean.ipynb`  
  Full Jupyter Notebook used during development and experimentation.
  Contains demo calls, visualizations, and debugging steps.

- `ai_agent.py`  
  Clean Python module that implements:
  - MySQL connection via SQLAlchemy  
  - Google Gemini initialization  
  - Prompt construction with database schema  
  - `ask_agent_llm(question)` helper to go from question → SQL → DataFrame

- `prompts.txt`  
  The base system prompt used for the Text-to-SQL agent:
  - schema description  
  - safety rules (read-only)  
  - example questions and SQL queries  

## Requirements

- Python 3.10+
- Libraries:
  - `pandas`
  - `sqlalchemy`
  - `pymysql` (or mysqlclient)
  - `google-generativeai`

Install via:

```bash
pip install pandas sqlalchemy pymysql google-generativeai
