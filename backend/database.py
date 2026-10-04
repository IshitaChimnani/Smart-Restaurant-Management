import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            items JSON NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            status VARCHAR(50) DEFAULT 'Preparing'
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM menu")

    count = cursor.fetchone()[0]

    if count == 0:

        menu_items = [
            ("Paneer Tikka", "Starter", 180),
            ("Veg Biryani", "Main Course", 220),
            ("Masala Dosa", "South Indian", 120),
            ("Cold Coffee", "Beverage", 100)
        ]

        cursor.executemany(
            """
            INSERT INTO menu
            (name, category, price)
            VALUES (%s, %s, %s)
            """,
            menu_items
        )

    conn.commit()

    cursor.close()
    conn.close()