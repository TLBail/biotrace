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
mkdir ftp-tests
echo "config" > ftp-tests/config
echo "data" > ftp-tests/data
echo "logs" > ftp-tests/logs
echo "tmp" > ftp-tests/tmp
echo "uploads" > ftp-tests/uploads
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