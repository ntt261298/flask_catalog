# MQ final project: Flask Catalog

### Installation and setup
Install [Python 3.9](https://www.python.org/downloads/release/python-396/), [pip](https://pypi.org/project/pip/) and clone this project:

    git clone https://github.com/ntt261298/flask_catalog.git
    
Setup the virtual environment:

    pip install virtualenv
    virtualenv env
    source env/bin/activate
    
Install the requirement:
    
    pip install -r requirements.txt
    
### Run app
Local

    ENV=local python run.py

Development

    ENV=development python run.py

Production

    ENV=production python run.py
    
### Run tests
Without coverage

    pytest tests/* 
    
With coverage

    pytest --cov=main tests/*

    
### Database setup
Install [mysql](https://dev.mysql.com/downloads/mysql/) and run the server:
    
    mysql.server start

Create local and test database:

    mysql -u root -p
    create database flask_catalog
    create database flas_catalog_test
    
Init migration repository
    
    flask db init

Create database migration:
    
    flask db migrate
    
Apply migration to database:

    flask db upgrade

    
    


