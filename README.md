# Hirola[![Maintainability](https://api.codeclimate.com/v1/badges/9c2bfbaf1910b72134d6/maintainability)](https://codeclimate.com/github/JamesKirkAndSpock/Hirola/maintainability)[![Coverage Status](https://coveralls.io/repos/github/JamesKirkAndSpock/Hirola/badge.svg)](https://coveralls.io/github/JamesKirkAndSpock/Hirola)[![CircleCI](https://circleci.com/gh/JamesKirkAndSpock/Hirola.svg?style=svg)](https://circleci.com/gh/JamesKirkAndSpock/Hirola)[![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com)

## Setup Application for Development

=> This Setup Assumes that you are using a Mac machine.

#### STEP 1: Clone the repository to your machine

Set up a directory where you will clone the repository. In this case we use the name "webapp" but you can choose any name you would want. Move into the created directory and clone the repository.

```
mkdir ~/webapp 
cd ~/webapp
git clone https://github.com/JamesKirkAndSpock/Hirola.git
```

#### STEP 2: Create a virtual environment and install requirements for the application

The next step involves creating a virtual environment separate from your own machine environment since we do not want to install any items that you do not need to be permanent in our machine. To do this however, you require to have Python3, pip and virtualenv already installed in your machine. We start by changing directory into Hirola. 

```
cd Hirola
```
We then create a virtual environment called hi-venv. The name is important to be spelt as is because it has been added to .gitignore file, meaning that we do not desire to push it remotely to github.
```
virtualenv --python=python3 hi-venv
```
We activate this virtual environment by running the command below. From now own you will not need to create a virtual environment again everytime you want to start your application. If the hi-venv folder is already there you will only be running the command below to activate the virtual environment. You should see the word `(hi-venv)` on your terminal after activating the virtual environment.
```
source hi-venv/bin/activate
```
We then install requirements for the applicaition by running the command below
```
pip install -r hirola/requirements.txt
```
To deactivate the virtual environment when not using the application just run the command below:
```
deactivate
```

This application uses [memcached](https://memcached.org/) to cache data on the application. You'll therefore need to install it and run it on the background.
```
brew install memcached
memcached -d
```

#### STEP 3: Set up postgres locally on your machine and creating a database

You can download postgres for Mac from [here](https://www.postgresql.org/download/macosx/). Create a postgres user and password and create a database to which will be added in the fourth step.

#### STEP 4: Setting up the .env variables and activating it.
To start the application some data may be needed that may change from one machine to another depending on the preference of the developer or the type of machine he or she is using. This data is placed in the .env file
Ensure you are just under the directory Hirola and create the file below.

```
touch .env
```

Open the file in you editor and fill in the information below.
```
export IP_ADDRESS=127.0.0.1
export HOST="localhost"
export DATABASE_NAME=<name of your postgres database>
export USER=<name of your postgres user>
export PASSWORD=<password of postgres user>
export DJANGO_SETTINGS_MODULE=hirola.settings.development
export POSTGRES_IP=127.0.0.1
export SECRET_KEY=<any random long string>
export CACHE_IP=127.0.0.1
export CACHE_PORT=11211
```
* The IP_ADDRESS refers to the address of localhost which is usually 127.0.0.1
* The HOST refers to the name pointing to the IP address which is usually localhost
* The DATABASE_NAME refers to the name of your postgres database
* The USER refers to the user who has access to your postgres database. Ensure that the user you give has priviledges of creating a database. This is because while django is running tests it creates a database before executing the tests and then drops it. The database user hence has to have these priviledges.
* The PASSWORD refers the the password of the user of your postgres database
* The DJANGO_SETTINGS_MODULE refers to the type of settings that will be used for the application where in this case we use settings in the development.py file for development by using the variable "hirola.settings.development"
* The POSTGRES_IP is the IP Address of which postgres will be accessed with. In development since postgres will be stored locally whe use the localhost IP Address.
* The SECRET_KEY is any random long string that will be used to generate the CSRF Token and can include any characters.
* The CACHE_IP refers to the address of the machine that you are running on. This should be the same as IP address.
* The CACHE_PORT refers to the port on which memcache is running. By default it runs on the Port 11211

Once you have entered data as per your machine and credentials for postgres you can save the file.

Source the file to place it as an environment variable
```
source .env
```

#### STEP 5: Start the application

* Change directory into the folder with the manage.py file
```
cd hirola
```
* Make migrations for the application
```
python manage.py makemigrations front
```
* Migrate the database.
```
python manage.py migrate front
```
* Start the application
```
python manage.py runserver
```

#### STEP 6: Test the application

* The following application uses caching of data using memcached. It is therefore necessary to install it before running tests, otherwise the tests will fail.

* In your MAC run the command `brew install memcached` or if using an ubuntu machine `sudo apt-get install memcached`

* Run the command `memcached -d` to run memcached in the background.

* Simply run the command below under the folder with the file manage.py
```
python manage.py test
```
