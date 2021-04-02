# Running the application:

To run this example follow these steps:

1. Activate a virtual environment that contains the packages in 'requirements.txt'

2. Set a FLASK_CONFIG environment variable to development or production with the following line:
    + set FLASK_ENV=development

3. Run the app with the following line:
    + flask run

The default settings of the app are drawn from an object in the config.py, you can alter
which settings are used by changing line 39 of \_\_init__.py


# Objective:

This Python Flask App was created to provide a Backend to an online blog website. It manages and persists blog posts,
users, and tags with SQLAlchemy.

Each blog Post consists of the following attributes:
1. Title
2. Date of Creation
3. A featured image
4. Text Content
5. A list of associated tags.

These are all accepted as key value pairs in the form of JSON. The _featured image_ is received in byte64 format as
a string. Converted into an image, given a unique name, and saved to the _img_ file. Then it's location is stored
as a string in the database.

The database 'flaskdatabase.db' can be created by the developer by running the following commands
within an active virtual environment containing the packages in 'requirements.txt':

+ python
+ from app.\_\_init__ import create_app
+ from app.extensions import db
+ db.create_all(app=create_app())
+ exit()

## Public Routes:
+ /single_blog/(post id as integer) - GET single blog in JSON format by its id attribute.
+ /all_blog_entries - GET all blog posts and associated tags in JSON format.
+ /tag/(tag as string) - GET all blog posts in JSON format with corresponding tag.
+ /admin - POST method accepts username and password in the form of JSON

## Private Routes:
The following can be accessed only after a successful log in via the '/admin' route.
+ /delete_entry/(post id as integer) - DELETE method removed post with corresponding id attribute.
+ /create_entry - POST method that creates a new post from JSON.
+ /update_entry/(post id as integer) - GET blog in JSON format by its id attribute. POST that updates blog from received JSON. 

# Security:

An admin login and password is created one time by the developer via commandline with a function
located on line 69 of \_\_init__.py

The password is salted and hashed using werkzeug library.

A successful login from user installs a authorization JSON Web Token in the browser's cookies.
This token expires after 15 minutes, but allows the admin access to specific routes that perform
CRUD operations on data stored within the database. These protected routes are located in 'private_views.py'

### Notable settings for production are:

+ 'JWT Cookie Secure' - If set to True the security cookies will only be sent to a browser via HTTPS connection
after a successful login.
+ 'JWT CSRF Protect' - If set to True a cookie 'csrf_access_token' is set in the browser when a user successfully
logs in, then when accessing protected routes, the csrf token's value must be returned.
The token is returned as a header with key: 'X-CSRF-TOKEN', and the value as the csrf token's contents.


# Application Structure

### Within the App folder you'll find the following files:

+ 'models' - Class files for the different databases used with the SQLAlchemy model.
+ 'static' - The img folder where all of the featured images are stored.
+ 'templates' - HTML templates that were created to test functionality of the app.

### Also the following files:

+ '\_\_init__.py' - Main 'create_app' function, registers blue prints and different extensions.
+ 'config.py' - Different config class files, these are settings uploaded depending on the object
selected in \_\_init__.py line 39
+ 'extensions.py' - The creation of the SQLAlchemy database and JWTManager.
+ 'private_views.py' - All the routes that can only be accessed with the JWT Token.
+ 'public_views.py' - All the routes that can be accessed publicly.
+ 'flaskdatabase.db' - The database created by SQLAlchemy

### Thank you for reading,
### Adam Combs
### Adamcombs1@gmail.com


