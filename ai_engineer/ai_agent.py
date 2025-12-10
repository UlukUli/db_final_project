"""
AI Text-to-SQL Agent for the Hotel Booking Database.

This module provides:
- MySQL connection via SQLAlchemy
- Google Gemini (Text-to-SQL) integration
- Helper functions to ask questions in natural language
  and get back pandas DataFrames.
"""

import os
import re
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text

import google.generativeai as genai

try:
    from config import GEMINI_API_KEY, MYSQL_URL
except ImportError:
    # Fallback: try environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://user:password@localhost/hotel_db")


# =========================
# 1. Database & LLM setup
# =========================

def get_engine():
    """
    Create and return a SQLAlchemy engine for the MySQL database.

    You can configure the URL either via:
      - config.py (MYSQL_URL), or
      - environment variable MYSQL_URL
    """
    engine = create_engine(MYSQL_URL)
    return engine


def init_gemini(model_name: str = "gemini-1.5-flash"):
    """
    Configure Google Gemini client.

    API key is taken from:
      - config.GEMINI_API_KEY, or
      - environment variable GEMINI_API_KEY
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to config.py or env.")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)
    return model


# =========================
# 2. Schema / prompt helpers
# =========================

def load_schema_description() -> str:
    """
    Returns a text description of the database schema
    to be injected into the LLM prompt.

    In the real project this can be generated dynamically
    from INFORMATION_SCHEMA, but here we provide a static
    schema overview for stability.
    """
    schema = """
You are a Text-to-SQL assistant for a MySQL database called hotel_booking.

Main fact table:
  bookings(booking_id, hotel_id, customer_id, room_id, meal_id,
           market_segment_id, distribution_channel_id, deposit_type_id,
           arrival_date_year, arrival_date_month, stays_in_week_nights,
           stays_in_weekend_nights, adr, is_canceled)

Dimension tables:
  hotels(hotel_id, hotel_type)
  customers(customer_id, country, customer_type, is_repeated_guest)
  rooms(room_id, room_code)
  market_segments(market_segment_id, market_segment)
  distribution_channels(distribution_channel_id, channel)
  meals(meal_id, meal)
  deposit_types(deposit_type_id, deposit_type)

Analytical views:
  view_cancel_rates(hotel_type, total_bookings, canceled, cancel_rate)
  view_monthly_occupancy(arrival_date_month, hotel_type, total_bookings)
  view_room_popularity(room_code, total_bookings)
  view_revenue_segments(market_segment, revenue)
  view_meal_plan_adr(meal, hotel_type, avg_adr)
"""
    return schema


def build_prompt(user_question: str) -> str:
    """
    Build the prompt for the LLM:
    - includes DB schema
    - includes instructions
    - asks the model to output ONLY SQL (no commentary)
    """
    schema = load_schema_description()
    prompt = f"""
You are an expert SQL assistant for a hotel booking MySQL database.

{schema}

TASK:
- Given the user question below, write ONE valid MySQL query.
- Only use tables and columns that exist in the schema.
- Prefer using the analytical views when possible (view_*).
- Do NOT modify data (no INSERT, UPDATE, DELETE, DROP).
- Return ONLY the SQL query, without ```sql``` markers or explanations.

User question:
\"\"\"{user_question}\"\"\"
"""
    return prompt


# =========================
# 3. LLM: Question -> SQL
# =========================

def extract_sql_from_text(text_out: str) -> str:
    """
    Extracts the SQL query from the model output:
    - removes ```sql ... ``` wrappers if present
    - strips extra text
    """
    # Try to capture inside code fences first
    fenced = re.findall(r"```sql(.*?)```", text_out, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        sql = fenced[0].strip()
    else:
        sql = text_out.strip()

    # Heuristic: stop at first semicolon if there is extra commentary
    if ";" in sql:
        sql = sql.split(";")[0] + ";"

    return sql


def question_to_sql_llm(model, question: str) -> str:
    """
    Sends the question + schema prompt to Gemini
    and returns a clean SQL string.
    """
    prompt = build_prompt(question)
    response = model.generate_content(prompt)
    raw_text = response.text or ""
    sql = extract_sql_from_text(raw_text)
    return sql


# =========================
# 4. SQL execution helpers
# =========================

def run_sql(engine, sql: str) -> pd.DataFrame:
    """
    Execute SQL and return a pandas DataFrame.
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)
    return df


def ask_agent_llm(question: str,
                  engine=None,
                  model=None,
                  verbose: bool = True) -> Optional[pd.DataFrame]:
    """
    High-level helper:
      1) question -> LLM -> SQL
      2) execute SQL -> DataFrame

    Returns a DataFrame with the result or None if an error occurs.
    """
    if engine is None:
        engine = get_engine()
    if model is None:
        model = init_gemini()

    if verbose:
        print(f"[Gemini] USER QUESTION:\n{question}\n")

    sql = question_to_sql_llm(model, question)

    if verbose:
        print("Generated SQL:\n")
        print(sql)
        print()

    try:
        df = run_sql(engine, sql)
    except Exception as e:
        print(f"[ERROR] Failed to execute SQL: {e}")
        return None

    if verbose:
        print("Result preview:")
        print(df.head())

    return df


if __name__ == "__main__":
    # Small manual demo (optional)
    engine = get_engine()
    model = init_gemini()

    q = "What is the cancellation rate by hotel type?"
    df_demo = ask_agent_llm(q, engine=engine, model=model, verbose=True)
