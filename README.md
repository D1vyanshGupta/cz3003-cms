# CZ3003 - Crisis Management System [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
The CMS provide real-time status updates on a map of Singapore, integrated with weather conditions, dengue hot spot, haze information and so on, on a web graphical user interface.

## Installation
Clone this repository into your local machine
```
git clone https://github.com/D1vyanshGupta/cz3003-cms.git
cd cz3003-cms
```
Activate virtual development environment
```
source venv/bin/activate
```
### 1. Requirement packages
```
pip install -r requirements.txt
```
### 2. PostgreSQL
PostgreSQL can be installed using [Homebrew](http://brew.sh/)

Install PostgreSQL
```
brew doctor && brew update && brew install postgresql
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
```

Create two new aliases to start and stop your postgres server
```
alias pg_start="launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist"
alias pg_stop="launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist"
```

Run the alias you just created: `pg_start` to start the database service

Create a user
```
createuser -s <user_name>
```

Create your postgres and connect to your postgres
```
createdb <user_name>
psql
```

Create project's database
```
CREATE DATABASE cms;
```


### 3. Redis
Redis can be installed via [Homebrew](http://brew.sh/)
```
brew install redis
```

### 4. Gdal
```
brew install gdal
```
- _The installation might take a while_


## Deployment
Go to project source code directory
```
cd src
```

Migrate django's models into database schema
```
python manage.py migrate
```

Run a celery worker in the background
```
celery -A cms worker -l info
```

Host django web service on your local machine
```
python manage.py runserver
```

