# Flask Cafe

A Python and Flask app for managing cafes and users, allowing users to favorite particular cafes and view their locations on a map. Starter code provided by [Rithm School](https://www.rithmschool.com/). Pair programmed with [Mara Greene](https://github.com/mrgjune).

It focuses on:

* many-to-many relationships in SQLAlchemy
* having Flask run JSON API routes
* Jinja templates and validation with WTForms
* [MapQuest Static Map API](https://developer.mapquest.com/documentation/static-map-api/v5/) integration 

## Installation

1. Clone this repository and cd into the flask-cafe folder. In order to make the MapQuest API work you need to set an environment variable `MAPQUEST_API_KEY=<your-key>`

2. Make a virtual environment, install Flask, and add the project dependencies: 

```
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install -r requirements.txt
```

3. Setup and seed the database: 

```
createdb flaskcafe    
python seed.py
```

Seed the DB on Heroku
```
DATABASE_URL=$(heroku config:get DATABASE_URL -a stephaniesimms-flask-cafe) python seed.py
```

4. Start the server:  

```
MAPQUEST_API_KEY=<your-key> flask run
```   
This will run the app on http://127.0.0.1:5000/ 

## Running Tests

1. Create test database:
 
```
createdb flaskcafe-test
```

2. Run tests:

```
python -m unittest -v tests  - to run all tests verbosely    
python -m unittest -v tests.CafeViewsTestCase  - to run tests for a specific model     
python -m unittest -v tests.CafeViewsTestCase.test_list  - to run a specific test 
```
