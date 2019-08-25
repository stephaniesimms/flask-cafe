A Python and Flask app for managing cafes and users, allowing users to favorite particular cafes and view their locations on a map. Starter code provided by [Rithm School](https://www.rithmschool.com/), pair programmed with [Mara Greene](https://github.com/mrgjune).

It focuses on:

* many-to-many relationships in SQLAlchemy
* high-coverage testing
* good software design for web applications & OO thinking in models
* consuming an API
* having Flask run JSON API routes
* Jinja templates and validation with WTForms
* [MapQuest Static Map API](https://developer.mapquest.com/documentation/static-map-api/v5/) integration 

## Installation
 Make a virtual environment and add the project dependencies: 
 
`mkvirtualenv flask-cafe`      
`pip install -r requirements.txt`

Setup and seed the database: 

`createdb flaskcafe`    
`python seed.py`         

Start the server:  

`flask run`   

## Testing

Create test database:
 
`createdb flaskcafe-test`

Run tests:

`python -m unittest -v tests`  - to run all tests verbosely    
`python -m unittest -v tests.CafeViewsTestCase`  - to run tests for a specific model     
`python -m unittest -v tests.CafeViewsTestCase.test_list`  - to run a specific test      
