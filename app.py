# app.py
from flask import Flask, request # <-- Add 'request'
import mysql.connector

app = Flask(__name__)

# Database configuration
DB_HOST = '192.168.64.9'
DB_USER = 'ping_user'
DB_PASSWORD = 'your_password'
DB_NAME = 'pings_db'

@app.route('/ping')
def ping():
    try:
        # Get the source IP from Nginx's proxy header
        ip_address = request.headers.get('X-Real-IP')

        # Connect to MySQL
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Insert a new record with the timestamp and IP address
        cursor.execute("INSERT INTO pings (timestamp, ip_address) VALUES (NOW(), %s);", (ip_address,))
        conn.commit()

        # Get the total count of pings
        cursor.execute("SELECT COUNT(*) FROM pings;")
        total_pings = cursor.fetchone()[0]

        # Close the connection
        cursor.close()
        conn.close()

        # Return the response
        return f"Pong."

    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
