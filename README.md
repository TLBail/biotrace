# biotrace
Application permettant le suivi des installations d'un méthaniseur

## Auteurs:
Théo LE BAIL
Thomas LEBRETON
Romain PIPON

## Requirements

- python3.10
- MariaDB/MySQL database

## Installation

Il faut installer le connector MariaDB sur la machine. 
Doc : https://mariadb.com/docs/server/connect/programming-languages/c/install/

`sudo apt install libmariadb3 libmariadb-dev`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database

Vous devez avoir MariaDB ou MySQL installé sur votre machine.
Une fois installé, vous devez créer une base de données.

```bash
mariadb < db/schema.sql
```

Pour remplir la base de données avec des données de test, vous pouvez exécuter le script suivant:

```bash
mariadb < db/data.sql
```


## Usage

```bash
pipenv run dev
```

## Tests

### FTP

Pour tester le FTP, vous pouvez utiliser le serveur FTP suivant:

```bash
mkdir -p ftp-tests/CONFIG ftp-tests/ALARM ftp-tests/LOG ftp-tests/BIN ftp-tests/CERT ftp-tests/DATA ftp-tests/CMD ftp-tests/DEF ftp-tests/SCRIPT
echo '; last modified 1 April 2001 by John Doe
[owner]
name = John Doe
organization = Acme Widgets Inc.

[database]
; use IP address in case network name resolution is not working
server = 192.0.2.62     
port = 143' > ftp-tests/CONFIG/config.ini
```


```bash
docker pull bogem/ftp
docker run --rm -it --init -v ./ftp-tests:/home/vsftpd \
				-p 2020:20 -p 2121:21 -p 47400-47470:47400-47470 \
				-e FTP_USER=admin \
				-e FTP_PASS=admin \
				-e PASV_ADDRESS=127.0.0.1 \
				--name ftp \ 
				bogem/ftp
```