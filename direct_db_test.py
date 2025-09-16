import sqlite3
import os
from datetime import datetime, timedelta

def main():
    # Path to the SQLite database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the farm_weatheralert table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='farm_weatheralert'")
        if not cursor.fetchone():
            print("Error: farm_weatheralert table does not exist. Please run migrations first.")
            return
            
        # Count existing alerts
        cursor.execute("SELECT COUNT(*) FROM farm_weatheralert")
        count = cursor.fetchone()[0]
        print(f"Found {count} weather alerts in the database.")
        
        # Add sample alerts if none exist
        if count == 0:
            print("Adding sample weather alerts...")
            now = datetime.now()
            
            sample_alerts = [
                ('तेज हवाओं की चेतावनी', 'आज शाम 5 बजे से रात 10 बजे तक 40-50 किमी/घंटा की रफ्तार से तेज हवाएं चलने की संभावना है।', 'storm', 'medium', now - timedelta(hours=2), now + timedelta(hours=8), 'दिल्ली और आसपास के इलाके'),
                ('गर्मी की लहर', 'अगले 3 दिनों तक तापमान 42-45 डिग्री सेल्सियस तक पहुंचने की संभावना है।', 'heatwave', 'high', now - timedelta(hours=1), now + timedelta(days=3), 'उत्तरी भारत')
            ]
            
            cursor.executemany("""
                INSERT INTO farm_weatheralert 
                (title, description, alert_type, severity, valid_from, valid_until, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, sample_alerts)
            
            conn.commit()
            print("Successfully added sample weather alerts.")
            
            # Display the added alerts
            cursor.execute("SELECT * FROM farm_weatheralert")
            print("\nCurrent weather alerts:")
            print("-" * 80)
            for row in cursor.fetchall():
                print(f"ID: {row[0]}")
                print(f"Title: {row[1]}")
                print(f"Type: {row[3]}")
                print(f"Severity: {row[4]}")
                print(f"Valid from: {row[5]}")
                print(f"Valid until: {row[6]}")
                print(f"Location: {row[7]}")
                print(f"Description: {row[2]}")
                print("-" * 80)
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
