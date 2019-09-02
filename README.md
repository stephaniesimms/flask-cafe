# Flask Cafe

A Python and Flask app for managing cafes and users, allowing users to favorite particular cafes and view their locations on a map. Starter code provided by [Rithm School](https://www.rithmschool.com/). Pair programmed with [Mara Greene](https://github.com/mrgjune).

It focuses on:

* many-to-many relationships in SQLAlchemy
* having Flask run JSON API routes
* Jinja templates and validation with WTForms
* [MapQuest Static Map API](https://developer.mapquest.com/documentation/static-map-api/v5/) integration 

## Installation

1. Make a virtual environment and add the project dependencies: 
 
```
mkvirtualenv flask-cafe       
pip install -r requirements.txt
```

2. Setup and seed the database: 

```
createdb flaskcafe    
python seed.py
```

3. Start the server:  

```
flask run
```   

## Testing

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
