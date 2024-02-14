import mariadb
import os
import time


class Database:
	def __init__(self):
		self.config = {
			'host': os.getenv('DB_HOST', 'localhost'),
			'port': int(os.getenv('DB_PORT', 3306)),
			'user': os.getenv('DB_USER', 'dev'),
			'password': os.getenv('DB_PASSWORD', 'dev'),
			'database': os.getenv('DB_NAME', 'Biotrace')
		}

		self.attempts = 10
		self.connect()

		# self.conn = mariadb.connect(**self.config)
		# self.cur = self.conn.cursor()

	def connect(self):
		for _ in range(self.attempts):
			try:
				self.conn = mariadb.connect(**self.config)
				self.cur = self.conn.cursor()
				break
			except mariadb.Error as e:
				print(f"Error: {e}")
				print("Retrying in 5 seconds...")
				time.sleep(5)
		else:
			print("Failed to connect to the database")
			exit(1)




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

	def get_logs(self, n = 10):
		self.cur.execute("SELECT id, type, name, CONVERT(content USING utf8) as content, created_at, updated_at, deleted_at FROM file WHERE type='log' AND deleted_at IS NULL ORDER BY id DESC LIMIT ?", (n,))
		rows = self.cur.fetchall()

		return rows

	def add_log(self, name, content):
		try:
			self.cur.execute("INSERT INTO file (type, name, content, created_at, updated_at) VALUES ('log', ?, ?, now(), now())", (name, content))
			self.conn.commit()
		except mariadb.Error as e:
			print(f"Error: {e}")

	def __del__(self):
		self.conn.close()
