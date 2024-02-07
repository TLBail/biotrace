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

	def get_hashed_configs(self, n = 10, cols : list[str] = ["*"]):
		self.cur.execute(f"SELECT {cols[0] if cols == ['*'] else ', '.join(cols)} FROM file WHERE type='config' AND deleted_at IS NULL ORDER BY id DESC LIMIT {str(n)}")
		rows = self.cur.fetchall()

		return rows

	def get_configs(self, n = 10):
		self.cur.execute("SELECT id, type, name, CONVERT(content USING utf8) as content, created_at, updated_at, deleted_at FROM file WHERE type='config' AND deleted_at IS NULL ORDER BY id DESC LIMIT ?", (n,))
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
