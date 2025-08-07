"""
Database connection and utility functions for the DB Agent project.
Simplified version using direct PostgreSQL connection.
"""
import os
import psycopg2
from typing import Optional
from dotenv import load_dotenv
from colorama import Fore


def get_database_connection():
    """
    Get a direct PostgreSQL database connection.
    
    Returns:
        psycopg2.connection: Database connection or None if failed
    """
    load_dotenv()
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=os.environ.get("POSTGRES_PORT", "5432"),
            database="postgres",
            user="postgres",
            password=os.environ.get("POSTGRES_PASSWORD")
        )
        return conn
    except Exception as e:
        print(Fore.RED + f"Error connecting to database: {e}")
        return None


def setup_database_schema() -> bool:
    """
    Create the customers table if it doesn't exist.
    
    Returns:
        bool: True if setup was successful, False otherwise
    """
    conn = get_database_connection()
    if not conn:
        return False
        
    try:
        with conn.cursor() as cur:
            # Create customers table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    bio TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            conn.commit()
            print(Fore.GREEN + "Database schema setup completed!")
            return True
            
    except Exception as e:
        print(Fore.RED + f"Error setting up database schema: {e}")
        return False
    finally:
        conn.close()


def seed_database() -> bool:
    """
    Seed the database with sample customer data.
        
    Returns:
        bool: True if seeding was successful, False otherwise
    """
    conn = get_database_connection()
    if not conn:
        return False
        
    try:
        with conn.cursor() as cur:
            # Check if data already exists
            cur.execute("SELECT COUNT(*) FROM customers")
            count = cur.fetchone()[0]
            
            if count > 0:
                print(Fore.YELLOW + "Database already contains data, skipping seed.")
                return True
                
            # Insert sample data
            sample_customers = [
                ("johndoe@gmail.com", "John Doe", "I am a software engineer"),
                ("janedoe@gmail.com", "Jane Doe", "I am a data scientist"),
                ("jimdoe@gmail.com", "Jim Doe", "I am a product manager"),
            ]
            
            cur.executemany(
                "INSERT INTO customers (email, full_name, bio) VALUES (%s, %s, %s)",
                sample_customers
            )
            conn.commit()
            print(Fore.GREEN + f"Successfully seeded database with {len(sample_customers)} customers")
            return True
            
    except Exception as e:
        print(Fore.RED + f"Error seeding database: {e}")
        return False
    finally:
        conn.close()
