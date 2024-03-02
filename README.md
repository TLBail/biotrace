# Biotrace

[![Python tests](https://github.com/TLBail/biotrace/actions/workflows/modbus-tests.yml/badge.svg)](https://github.com/TLBail/biotrace/actions/workflows/modbus-tests.yml)

Application permettant le suivi des installations d'un méthaniseur

## Auteurs:

- Théo LE BAIL <https://github.com/TLBail>
- Thomas LEBRETON <https://github.com/tholeb>
- Romain PIPON <https://github.com/Sh1nc0>

## Requirements

- python3.10
- MariaDB/MySQL database
- pipenv

## Installation

### Connector MariaDB

Il est nécessaire d'installer un connecter. Pour cela, vous pouvez utiliser les paquets suivants :

#### CentOS, RHEL, Rocky Linux
```bash
sudo yum install MariaDB-shared MariaDB-devel
```

#### Debian, Ubuntu
```bash
sudo apt install libmariadb3 libmariadb-dev
```

*Doc <https://mariadb.com/docs/server/connect/programming-languages/c/install/#Installation_via_Package_Repository_(Linux)>*

*Note: L'installation du connector est à faire **avant** l'installation des paquets.*

### Python

```bash
pipenv install
```

### Base de données

Vous devez avoir MariaDB ou MySQL installé sur votre machine.
Une fois installé, vous devez créer une base de données.

```bash
mariadb < db/schema.sql < db/procedure-cleanup.sql < db/trigger-configs.sql
```

## Usage

```bash
pipenv run dev
```

## Dev

Pour exécuter automatiquement certains tests avant chaque commit :

```sh
git config --local include.path ../.gitconfig
```

### Base de données

Pour remplir la base de données avec des données de test, vous pouvez exécuter le script suivant:

```bash
mariadb < db/data.sql
```

Et pour ajouter un utilisateur de test *(dev:dev)*

```bash
mariadb < db/dev.sql
```

### FTP

Pour tester le FTP, vous pouvez utiliser le serveur FTP suivant:

```bash
mkdir -p /tmp/ftp-tests/CONFIG /tmp/ftp-tests/ALARM /tmp/ftp-tests/LOG /tmp/ftp-tests/BIN /tmp/ftp-tests/CERT /tmp/ftp-tests/DATA /tmp/ftp-tests/CMD /tmp/ftp-tests/DEF /tmp/ftp-tests/SCRIPT
echo '; last modified 1 April 2001 by John Doe
[owner]
name = John Doe
organization = Acme Widgets Inc.

[database]
; use IP address in case network name resolution is not working
server = 192.0.2.62   
port = 143' > /tmp/ftp-tests/CONFIG/config.ini
```

```bash
docker pull bogem/ftp
docker run --rm -it --init -v /tmp/ftp-tests:/home/vsftpd \
				-p 2020:20 -p 2121:21 -p 47400-47470:47400-47470 \
				-e FTP_USER=admin \
				-e FTP_PASS=admin \
				-e PASV_ADDRESS=127.0.0.1 \
				--name ftp \ 
				bogem/ftp
```
