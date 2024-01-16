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

    def __del__(self):
        self.conn.close()
