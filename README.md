# FlaskWebServerSimple
Created a simple Flask web server with user authentication and error handling that scrapes predetermined websites for information and stores in persistent storage. 

Note: I did not post API keys for privacy reasons.
Note: Also, the web server can be accessed via web browser but there is no GUI. It is meant to be used with the curl command.

Scraper Functionality:

-Creates a Flask server with authentication. All functions require user authentication.

-Creates pymongo server.

-Password Function: Checks a username and password. There is an admin default login or user searches mongoDB database for password with username.

-Login Function: Requires an initial login put accepts new user creation and stores in MongoDB.

-Weather Function: Uses OpenWeatherMap API to find the weather in a user inputted city.

-COVID Scraper: Scrapes the worldometers site for COVID information in a user inputted state.

Services Functionality:

-Creates a different Flask server with authentication and also makes all functions require authentication.

-Same login function as the server.

-Weather and COVID funcitons take user input and communicates with the Scraper server via requests for information.

-Marvel Function: Uses Marvel's API to get information about a user specified character. Requires a hashkey.
