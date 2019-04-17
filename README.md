# Capstone Project - Broward Exchange

## Group
- Heather
- Jay
- Jorge

This project uses pipenv to manage the python virtual environment and the project's dependencies.

To start the project using Flask, set the FLASK_APP environment variable to the app.py file. Then run 'flask run' from a terminal.

To start the project using uWSGI, run 'uwsgi website_uwsgi.ini' to start with the configuration specified in the ini file. Uncomment the protocol line to have uWSGI serve http on the specified port, otherwise, the output is meant for a webserver.
