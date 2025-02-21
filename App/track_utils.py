import sqlite3
from datetime import datetime

# Database connection
def connect_db():
    conn = sqlite3.connect('app_data.db')  # Ensure the database is named correctly and exists in your project directory
    return conn

# Create tables if they don't exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create table for page visits tracking with the necessary columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS page_visited_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pagename TEXT NOT NULL,
                        visit_time TEXT NOT NULL)''')

    # Create table for storing prediction details with necessary columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS prediction_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        raw_text TEXT NOT NULL,
                        prediction TEXT NOT NULL,
                        probability REAL NOT NULL,
                        time_of_visit TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

# Add details of the page visit
def add_page_visited_details(pagename, visit_time):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Insert page visit details into the table
    cursor.execute("INSERT INTO page_visited_details (pagename, visit_time) VALUES (?, ?)", 
                   (pagename, visit_time))
    conn.commit()
    conn.close()

# View all page visited details
def view_all_page_visited_details():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT pagename, visit_time FROM page_visited_details")
    rows = cursor.fetchall()
    conn.close()
    
    return rows

# Add details of the prediction
def add_prediction_details(raw_text, prediction, probability, time_of_visit):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert prediction details into the table
    cursor.execute("INSERT INTO prediction_details (raw_text, prediction, probability, time_of_visit) VALUES (?, ?, ?, ?)", 
                   (raw_text, prediction, probability, time_of_visit))
    conn.commit()
    conn.close()

# View all prediction details
def view_all_prediction_details():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT raw_text, prediction, probability, time_of_visit FROM prediction_details")
    rows = cursor.fetchall()
    conn.close()
    
    return rows

# Create the necessary tables when the script is run
create_tables()
