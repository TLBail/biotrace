from argparse import ArgumentParser
from ftplib import FTP
import mariadb
import sys
import hashlib
from Database import Database
from base64 import b64encode


p = ArgumentParser(description="Récupère un fichier depuis un serveur FTP et le stocke dans une base de données")

ftp_group = p.add_argument_group("FTP")
ftp_group.add_argument("hostname", help="FTP server hostname", default="localhost")
ftp_group.add_argument("username", help="FTP username", default="admin")
ftp_group.add_argument("password", help="FTP password", default="admin")
ftp_group.add_argument("-P", "--port", type=int, default=21, help="FTP server port")

p.add_argument("-f", "--file", help="(remote) file path", required=True)
p.add_argument("-o", "--option", choices=("pull", "push"), default="pull", help="Action to perform")
args = p.parse_args()

def get_md5(file):
    md5 = hashlib.md5()

    with open(file, "rb") as obj:
        for part in iter(lambda: obj.read(4096), b""):
            md5.update(part)

    return md5.hexdigest()


with FTP() as ftp:
	ftp.connect(args.hostname, args.port)
	ftp.login(args.username, args.password)
	print("connected to ftp")
	ftp.cwd("/")
	if args.option == "pull":
		with open(args.file, "wb") as f:
			ftp.retrbinary(f"RETR {args.file}", f.write)
			print("file downloaded")

db = Database()

file_md5 = get_md5(args.file)

configs = db.get_hashed_configs(cols = ["MD5(content)"])

if (file_md5,) in configs:
	print("file already in database")
else:
	with open(args.file, "rb") as f:
		content = f.read()
		db.add_config("config", content)
		print("file added to database")

