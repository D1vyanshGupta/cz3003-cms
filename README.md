# CZ3003 - Crisis Management System [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
The CMS provide real-time status updates on a map of Singapore, integrated with weather conditions, dengue hot spot, haze information and so on, on a web graphical user interface.

## Installation
Clone this repository into your local machine
```
git clone https://github.com/D1vyanshGupta/cz3003-cms.git
cd cz3003-cms
```
Activate virtual development environment
- MacOS
```
source venv/bin/activate
```
- Windows
```
venv/Scripts/activate
```
### 1. Requirement packages
```
pip install -r requirements.txt
```
### 2. PostgreSQL
#### MacOS
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

#### Windows
Download and run the [PostgreSQL Installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- Ensure that the installation includes the PostgreSQL Unicode ODBC driver
- During installation, set up a user account with superuser privileges.

Add the PostgreSQL bin directory path to the `PATH` environmental variable.

Open the psql command-line tool
```
psql
```

In the Windows Command Prompt, run the command
```
psql -U <user_name>
```

Create project's database
```
CREATE DATABASE cms;
```

### 3. Redis
#### MacOS
Redis can be installed via [Homebrew](http://brew.sh/)
```
brew install redis
```

#### Windows
Download and install [Redis-x64-3.0.504.msi](https://github.com/MicrosoftArchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi)

After the redis service is installed, we can operate it from `Service manager`

![Image](https://i.stack.imgur.com/nCwcR.png)

### 4. Gdal
#### MacOS
```
brew install gdal
```
- _The installation might take a while_

#### Windows
Download the [32bit](http://download.osgeo.org/osgeo4w/osgeo4w-setup-x86.exe) or [64bit](http://download.osgeo.org/osgeo4w/osgeo4w-setup-x86_64.exe) OSGeo4W network installer.

Run the installer, then select `Express Install`, and `Next`.

Pick `Gdal` package to install, and `Next`.

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

