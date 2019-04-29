# Capstone Project - Broward Exchange

## Group
- Heather
- Jay
- Jorge

This project uses pipenv to manage the python virtual environment and the project's dependencies.

Installing using "pipenv install" will install all dependencies except for uWSGI. Using "pipenv install -dev" will include it but uWSGI is only supported on Linux systems.

Ngnix was used as the webserver for project but the webserver must know how to communicate with the uwsgi protocol and pass requests through. The included nginx.conf describes where the webserver will look for the static files. I used "mount --bind /project/file/location /srv/http" to allow the project to keep its files consolidated to its static folder while allowing the webserver to check whichever location we tell it to.

To start the project using Flask, set the FLASK_APP environment variable to the app.py file. Then run 'flask run' from a terminal.

To start the project using uWSGI, run 'uwsgi website_uwsgi.ini' to start with the configuration specified in the ini file. Uncomment the protocol line to have uWSGI serve http on the specified port, otherwise, the output is meant for a webserver.
