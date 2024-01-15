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