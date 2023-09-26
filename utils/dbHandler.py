import psycopg2

class dbHandler:
    def __init__(self, database, user, password, host, port) -> None:
        self.connection = psycopg2.connect(
            database = database,
            user = user,
            password = password,
            host = host,
            port = port
        )
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query, *args) -> bool:
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return False

    def fetch_one(self, query, *args) -> tuple:
        self.cursor.execute(query,args)
        return self.cursor.fetchone()
    
    def fetch_all(self, query, *args) -> list:
        self.cursor.execute(query,args)
        return self.cursor.fetchall()
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()
    
    def get_all(self):
        """
        Fetches all users' usernames, IDs, and their appointments sorted by user_id.

        Returns:
            list of tuples: A list of tuples containing (user_id, username, date, start_time, end_time, purpose) for each appointment.
        """
        query = """
            SELECT u.user_id, u.username, a.date, a.start_time, a.end_time, a.purpose
            FROM appointment_system.users u
            LEFT JOIN appointment_system.appointments a ON u.user_id = a.user_id
            ORDER BY u.user_id;
        """
        result = self.fetch_all(query)
        return result