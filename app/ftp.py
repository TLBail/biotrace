from argparse import ArgumentParser
from ftplib import FTP
import hashlib
from modules.Database import db_session, init_db, init_engine
from sqlalchemy import func
from models.File import File
from configparser import ConfigParser
from os import makedirs
from io import BytesIO

config = ConfigParser()
config.read('config.ini')

p = ArgumentParser(description="Récupère un fichier depuis un serveur FTP et le stocke dans une base de données")
p.add_argument("-v", "--verbose", action="store_true", help="Affiche les query SQL")
p.add_argument("-t", "--tmp", dest="tmp_dir", type=str, default="/tmp/biotrace_ftp/", help="Dossier ou seront uploadé les fichiers temporaires", metavar="/tmp/biotrace_ftp/")

subparsers = p.add_subparsers(title="Options", dest="subcommand", help="Action à effectuer", required=True)

# Subcommand 'push'
push_parser = subparsers.add_parser('push', help='Push d\'un fichier sur le serveur FTP')
push_parser.add_argument('-f', '--file_path', dest="file", type=str, help='Chemin vers lequel le fichier va être téléchargé', metavar="/CONFIG/config.ini", default="/CONFIG/config.ini", required=True)
push_parser.add_argument('-i', '--file_id', type=int, help='Le numéro du fichier dans la base de données', required=True)

# Subcommand 'pull'
pull_parser = subparsers.add_parser('pull', help='Pull d\'un fichier depuis le serveur FTP')
pull_parser.add_argument('-f', '--file_path', dest="file", type=str, help='Fichier qui va être téléchargé puis inséré dans la base de données', metavar="/CONFIG/config.ini", default="/CONFIG/config.ini", required=True)
pull_parser.add_argument("-n", "--file_name", type=str, help="Nom du fichier dans la base de données")

args = p.parse_args()

init_engine(f"mariadb+mariadbconnector://{config['database'].get('username', 'dev')}:{config['database'].get('password', 'dev')}@{config['database'].get('hostname', '127.0.0.1')}:{config['database'].getint('port', 3306)}/{config['database'].get('name', 'Biotrace')}", echo=args.verbose)
init_db()


def get_md5(file):
	md5 = hashlib.md5()

	with open(file, "rb") as obj:
		for part in iter(lambda: obj.read(4096), b""):
			md5.update(part)

	return md5.hexdigest()


with FTP() as ftp:
	ftp.connect(config['ftp'].get('hostname', '127.0.0.1'), config['ftp'].getint('port', 2121))
	ftp.login(config['ftp'].get('username', 'admin'), config['ftp'].get('password', 'admin'))
	print("connected to ftp")

	if args.subcommand == "pull":
		ftp.cwd("/".join(args.file.split("/")[:-1]) + "/")
		makedirs(args.tmp_dir, exist_ok=True)

		file_name = args.file.split("/")[-1]
		local_path = f"{args.tmp_dir}{'' if args.tmp_dir[-1] == '/' else '/'}{file_name}"

		with open(local_path, "wb") as f:
			def cb(data):
				f.write(data)
				print(f"downloaded {len(data)} bytes from {args.file} to {local_path}")

			ftp.retrbinary(f"RETR {file_name}", cb)

		file_md5 = get_md5(local_path)

		configs = db_session.query(func.md5(File.content)).all()

		if (file_md5,) in configs:
			print("file already in database")
		else:
			with open(local_path, "rb") as f:
				db_session.add(File(name=args.file_name or file_name, type="config", content=f.read().decode("utf-8")))
				db_session.commit()
				print("file added to database")

	elif args.subcommand == "push":
		config = db_session.query(File).filter_by(type='config', id=args.file_id).one_or_none()

		if config is None:
			print(f"No config with id {args.file_id} was found in the database.")
			exit(1)

		remote_path = f"{args.tmp_dir}{'' if args.tmp_dir[-1] == '/' else '/'}{config.name}"

		print(f"Found config with id #{config.id}")

		file_name = args.file.split("/")[-1]

		ftp.cwd("/".join(args.file.split("/")[:-1]) + "/")
		ftp.storbinary(f"STOR {file_name}", BytesIO(bytes(config.serialize()['content'], "utf8")), callback=lambda data: print(f"uploaded {len(data)} bytes"))
