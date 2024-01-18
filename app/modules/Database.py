import mariadb


class Database:
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'dev',
            'password': 'dev',
            'database': 'Biotrace'
        }

        self.conn = mariadb.connect(**self.config)
        self.cur = self.conn.cursor()

    def get_configs(self, n):
        self.cur.execute("SELECT * FROM file WHERE type='config' and deleted_at is NULL ORDER BY id DESC LIMIT " + str(n))
        rows = self.cur.fetchall()

        return rows

    def add_config(self, name, content):
        # try to insert
        try:
            self.cur.execute("INSERT INTO file (type, name, content, created_at, updated_at) VALUES ('config', ?, ?, now(), now())", (name, content))
            self.conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")

    def __del__(self):
        self.conn.close()
