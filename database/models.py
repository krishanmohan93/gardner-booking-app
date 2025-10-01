import sqlite3
from datetime import datetime

class DatabaseHelper:
    def __init__(self, db_path="garden_app.db"):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            user_type TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            bio TEXT,
            hourly_rate REAL,
            availability TEXT,
            rating REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create Services table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            base_price REAL
        )
        """)

        # Create Gardner Services table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS gardner_services (
            gardner_id INTEGER,
            service_id INTEGER,
            FOREIGN KEY (gardner_id) REFERENCES users (id),
            FOREIGN KEY (service_id) REFERENCES services (id),
            PRIMARY KEY (gardner_id, service_id)
        )
        """)

        # Create Bookings table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            gardner_id INTEGER,
            service_id INTEGER,
            booking_date TIMESTAMP NOT NULL,
            duration INTEGER,
            status TEXT DEFAULT 'pending',
            total_price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id),
            FOREIGN KEY (gardner_id) REFERENCES users (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
        """)

        conn.commit()
        conn.close()

    def add_user(self, username, email, password_hash, user_type, **kwargs):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, user_type, 
                         first_name, last_name, phone, bio, hourly_rate, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, email, password_hash, user_type,
              kwargs.get('first_name'), kwargs.get('last_name'),
              kwargs.get('phone'), kwargs.get('bio'),
              kwargs.get('hourly_rate'), kwargs.get('availability')))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id

    def get_user(self, username=None, email=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if username:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        else:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            
        user = cursor.fetchone()
        conn.close()
        return user

    def get_gardner_list(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, username, first_name, last_name, hourly_rate, rating, bio
        FROM users WHERE user_type = 'gardner'
        ORDER BY rating DESC
        """)
        
        gardners = cursor.fetchall()
        conn.close()
        return gardners

    def create_booking(self, client_id, gardner_id, service_id, booking_date, duration):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get gardner's hourly rate
        cursor.execute("SELECT hourly_rate FROM users WHERE id = ?", (gardner_id,))
        hourly_rate = cursor.fetchone()[0]
        total_price = hourly_rate * duration
        
        cursor.execute("""
        INSERT INTO bookings (client_id, gardner_id, service_id, booking_date, 
                            duration, total_price)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (client_id, gardner_id, service_id, booking_date, duration, total_price))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return booking_id

    def get_user_bookings(self, user_id, user_type='client'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_type == 'client':
            cursor.execute("""
            SELECT b.*, u.first_name, u.last_name, s.name as service_name
            FROM bookings b
            JOIN users u ON b.gardner_id = u.id
            JOIN services s ON b.service_id = s.id
            WHERE b.client_id = ?
            ORDER BY b.booking_date DESC
            """, (user_id,))
        else:
            cursor.execute("""
            SELECT b.*, u.first_name, u.last_name, s.name as service_name
            FROM bookings b
            JOIN users u ON b.client_id = u.id
            JOIN services s ON b.service_id = s.id
            WHERE b.gardner_id = ?
            ORDER BY b.booking_date DESC
            """, (user_id,))
            
        bookings = cursor.fetchall()
        conn.close()
        return bookings