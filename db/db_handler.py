import sqlite3

class DatabaseHandler:
    """
    Database handler class"""
    def __init__(self, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
    
    def create_table(self) -> None:
        """Creating table in database"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            event_detail TEXT NOT NULL
        )""")
        self.conn.commit()
    
    def list_table(self) -> list:
        """List table in database"""
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        data = self.cursor.fetchall()
        return data
    
    def add_event(self, year: str, month: str, day: str, start_time: str, end_time: str, event_detail:str) -> None:
        """Adding event to database"""
        self.cursor.execute("""INSERT INTO events (year, month, day, start_time, end_time, event_detail) VALUES (?, ?, ?, ?, ?, ?)""", (year, month, day, start_time, end_time, event_detail))
        self.conn.commit()
    
    def get_all_events(self) -> list:
        """Get all events from database"""
        self.cursor.execute("""SELECT * FROM events""")
        data = self.cursor.fetchall()
        return data
    
    def clear_all_events(self) -> None:
        """Clear all events from database"""
        self.cursor.execute("""DELETE FROM events""")
        self.conn.commit()

    def delete_event(self, id:list) -> list:
        """Delete event from database"""
        for i in id:
            self.cursor.execute("""DELETE FROM events WHERE id = ?""", (i))
        self.conn.commit()
    
    def find_event(self, query: str, year=None, month=None, day=None, start_time=None, end_time=None) -> list:
        """Find event in database
            At least one of the following parameters must be provided:
                - year
                - month
                - day
                - start_time
                - end_time
        """
        if not query:
            return []
        conditions = []
        values = []
        data = []
        if year:
            conditions.append("year = ?")
            values.append(year)
        if month:
            conditions.append("month = ?")
            values.append(month)
        if day:
            conditions.append("day = ?")
            values.append(day)
        if start_time:
            conditions.append("start_time = ?")
            values.append(start_time)
        if end_time:
            conditions.append("end_time = ?")
            values.append(end_time)
        
        if not conditions:
            return data
        query += " AND ".join(conditions)
        self.cursor.execute(query, tuple(values))
        data = self.cursor.fetchall()
        return data
    
    def update_event(self, id: str, year: str, month: str, day: str, start_time: str, end_time: str, event_detail:str) -> None:
        """Update event in database"""
        self.cursor.execute("""SELECT * FROM events
                            WHERE year = ? AND month = ? AND day = ? AND start_time <= ? AND end_time >= ? AND id != ?""",
                            (year, month, day, start_time, end_time, id))
        data = self.cursor.fetchall()
        if data:
            return
        self.cursor.execute("""UPDATE events SET year = ?, month = ?, day = ?, start_time = ?, end_time = ?, event_detail = ?
                            WHERE id = ?""", (year, month, day, start_time, end_time, event_detail, id))
        self.conn.commit()
    
    def is_time_available(self, year: str, month: str, day: str, start_time: str, end_time: str) -> bool:
        """Check if the given time is available"""
        self.cursor.execute("""SELECT * FROM events 
                            WHERE year = ? AND month = ? AND day = ? AND start_time <= ? AND end_time >= ?""",
                            (year, month, day, start_time, end_time))
        data = self.cursor.fetchall()
        if data:
            return False
        return True
    
    def close(self) -> None:
        """Close connection"""
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    ...