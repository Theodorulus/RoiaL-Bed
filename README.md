# RoiaL-Bed

## About

This is a backend application for a smart bed. 
The app was created to improve your sleep quality and help you relax more.

### Built With

<li><a href="https://www.python.org/"> Python </a></li>
<li><a href="https://flask.palletsprojects.com/en/2.0.x/"> Flask </a></li>
<li> <a href="https://docs.python-requests.org/en/latest/"> Requests</a> (for API calls to OpenWeather API)</li>
<li><a href="https://docs.pytest.org/en/6.2.x/"> Pytest </a> (for automation testing)</li>
<li> <a href="https://coverage.readthedocs.io/en/6.3/"> Coverage</a> (for automation testing coverage)</li>

## Getting Started

### Prerequirements
To run the app, you need to have <a href="https://www.python.org/downloads/"> Python </a> and <a href="http://www.steves-internet-guide.com/install-mosquitto-broker/"> Mosquitto MQTT Broker </a> installed on your system.
<br/>
To test the app's functionalities, you need to have an API platform for using APIs installed on your system. (For example: <a href="https://www.postman.com/downloads/">Postman</a>)


### Installation

0. Clone the repo
`git clone https://github.com/Theodorulus/RoiaL-Bed.git`

1. `cd into-this-project`

2. Install venv if not already installed:
`pip install virtualenv`

3. Create an environment:
`python -m venv venv`

4. Activate environment
`cd venv/Scripts`
`activate.bat`
`cd ../../`

5. Install libraries 
`pip install -r dependencies.txt`

6. Set environment value for development
`set FLASK_ENV=development`

### MQTT Broker
Install musquitto Mqtt broker, if you do not have one already, following: http://www.steves-internet-guide.com/install-mosquitto-broker/
Note: To run the mosquitto broker, you must enter `mosquitto` command in terminal at the mosquitto installation folder (by default being `C:\Program files\mosquitto`)


### Running the app
Because flask-mqtt cannot run multiple workers(threads) at the same time, and because the app has a main HTTP thread and another one for Mqtt, `flask run` command is of no use.
Instead, run:
`python app.py`


### Unit tests
To run unit tests, use 
`python -m pytest -v -m "not integrationTest"`

### Integration tests
To run integration tests, use 
`python -m pytest -v -m integrationTest`

To see tests coverage, use
`coverage run -m pytest -v`
`coverage report`

## Usage
This backend app is an API, so you need to have an API platform for using APIs installed on your system.

### MQTT functionalities
The app subscribes to the "smart_bed" topic of the broker connected to the local 1883 port. (the broker must be running -> see MQTT Broker section)
Having the mosquitto broker and the app running, open a new terminal and navigate to the mosquitto installation folder. There, run the command:
`mosquitto_sub -t smart_bed -v`
You now should be able to read the messages published by the app.

### Rest API HTTP functionalities
All of the Rest API HTTP functionalities can be found in the <a href="https://github.com/Theodorulus/RoiaL-Bed/blob/main/openapi.json">Open API documentation</a>.
To test them, you need to have the app running and call the API using your API platform app (Example: <a href="https://www.postman.com/"> Postman</a>).

## Roadman
See the <a href="https://github.com/Theodorulus/RoiaL-Bed/projects/1"> open issues </a> for the full list of features.

## Contribution

### Team Members

[Hîrhui Călin](https://github.com/cul1n)

[Smeu Ștefan](https://github.com/MrNiceGuy090)

[Tică Constantin](https://github.com/costi-tica)

[Tudorache Theodor](https://github.com/Theodorulus)

[Zaharia Cătălin](https://github.com/Catalin-Zaharia)

## Acknowledgments

<li> <a href="https://flask.palletsprojects.com/en/2.0.x/"> Flask documentation </a> </li>
<li> <a href="https://docs.pytest.org/en/6.2.x/contents.html"> Pytest documentation </a> </li>
<li> <a href="https://coverage.readthedocs.io/en/6.3/"> Coverage documentation </a> </li>
<li> <a href="https://openweathermap.org/api"> OpenWeather API </a> </li>
