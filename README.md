# Cool GeoApp API

Welcome to the GeoApp API! 
This is a test API that serves a web application for the turnovers of the Comunidad de Madrid
with information like customer gender, age, date or turnover amount, given a desired geometry.
The only requirement to run the application is to have installed Docker on your machine and
with a simple like ```sudo docker-compose up``` you should be ready to go.
It has been developed and tested under a Linux distribution (Ubuntu 20.04) but since Docker
takes care here of compatibility issues it should run under most OS's.
Both the API service and the database are defined in the ```docker-compose.yml``` file, which
contains the information about the images configuration, enviroments and commands to be run.
Please make sure you have the ports 5000 and 5432 of your machine free to use or change this
enviroment variables for the application to work. The ```init.sql``` will fill the database 
with the tables provided (paystats and postal_codes), creating the ```data``` folder.
For the API, the ```Dockerfile``` is in charge of the python dependecies installation via the
```requirements.txt``` file and to run the command that execute the root script of the 
application ```app.py```. This script serves as the controller of the app, who receives the
user requests that matches the entrypoints defined with the Flask framework, validate the
parameters preventing bad code and send the control to the model, in case database connection
was successfully done. The ```model.py``` is the intermediate bettween the entrypoints and 
the database. Here are defined the functions to connect to the db and to ask for the data in 
the tables throught raw SQL queries and the methods provided by the library ```psycopg2```.
And that is pretty much it. Easy, lightweight, scalable and portable.
Open your browser, type ```localhost:5000``` and you should be watching this:
```
{
  "status": "Database connection successfully"
}
```
This means everything is working properly and configuration stuff was overcome.
Next I'm going to try to explain the functionalities of the application. There are 3 
entrypoints in the app where you can get the data:

- Function to get the turnvoer by age and gender of a postal_code given longitude and
    latitude coordinates (first part) and a date (second part). Example:
    ```
        /-3.83 40.39/2015-04-01/
    ```
- Function to get the turnover by age and gender of the whole Comunidad de Madrid given
    a date. Example:
    ```
        /madrid/2015-04-15/
    ```
- Function to get the time serie of the turnovers of a postal_code given its coordinates,
    a starting date and a ending date. Example:
    ```
        /-3.83 40.39/2015-04-01 2015-09-01/
    ```

Many validation and error handling could be added here to make the app more robust but 
for the purpose of this test this code will do the job. I could have added an 
authentication system here if I had more time. I have used JSON Web Token for this task with
PHP and Node.js before and it works very well, so that is what I had used.

There is a lot of room for the improvement and I wish I had more spare time to develop it,
but I hope this shows you some of the skills that I have. Any question or consideration
I will be very willing to answer to you.

## Jesús Morán