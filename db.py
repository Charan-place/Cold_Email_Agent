import mysql.connector
from datetime import datetime
import os

def log_email(sender_email, recipient_email, job_description, email_body):
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_email VARCHAR(255),
            recipient_email VARCHAR(255),
            job_description TEXT,
            email_body TEXT,
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        INSERT INTO email_logs (sender_email, recipient_email, job_description, email_body, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """, (sender_email, recipient_email, job_description, email_body, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
