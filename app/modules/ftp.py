from argparse import ArgumentParser
from ftplib import FTP
import hashlib
from Database import Database


p = ArgumentParser(description="Récupère un fichier depuis un serveur FTP et le stocke dans une base de données")

ftp_group = p.add_argument_group("FTP")
ftp_group.add_argument("hostname", help="FTP server hostname", default="localhost")
ftp_group.add_argument("username", help="FTP username", default="admin")
ftp_group.add_argument("password", help="FTP password", default="admin")
ftp_group.add_argument("-P", "--port", type=int, default=21, help="FTP server port")

push_group = p.add_argument_group("Push")
push_group.add_argument("-f", "--file", help="(remote) file path (pull only)")

pull_group = p.add_argument_group("Pull")
pull_group.add_argument("-i", "--file_id", help="File's ID from the database (push only)")

p.add_argument("-o", "--option", choices=("pull", "push"), default="pull", help="Action to perform")
args = p.parse_args()

db = Database()


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

    if args.option == "pull":
        ftp.cwd("/".join(args.file.split("/")[:-1]) + "/")
        file_name = args.file.split("/")[-1]

        with open(file_name, "wb") as f:
            def cb(data):
                f.write(data)
                print(f"downloaded {len(data)} bytes")

            ftp.retrbinary(f"RETR {file_name}", cb)
    elif args.option == "push":
        file = db.get_config_by_id(args.file_id)
        print(file)

        if file is None:
            print("file not found")
            exit(1)

        ftp.storbinary(f"STOR {file.name}", file, callback=lambda data: print(f"uploaded {len(data)} bytes"))

if args.option == "pull":
    file_name = args.file.split("/")[-1]
    file_md5 = get_md5(file_name)

    configs = db.get_hashed_configs(cols=["MD5(content)"])

    if (file_md5,) in configs:
        print("file already in database")
    else:
        with open(file_name, "rb") as f:
            db.add_config(file_name, f.read())
            print("file added to database")
