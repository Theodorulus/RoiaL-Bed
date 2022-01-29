# RoiaL-Bed

### Instalation

1. `cd into this project`

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

### MQTT Broker:
  1) Install museqito Mqtt broker, if you do not have one already, following: http://www.steves-internet-guide.com/install-mosquitto-broker/
Note: To run the mosquitto broker, you must enter `mosquitto` command in terminal at the mosquitto installation folder (by default being "C:\Program files\mosquitto")


### Running the app:
Because flask-mqtt cannot run multiple workers(threads) at the same time, and because the app has a main HTTP thread and another one for Mqtt, `flask run` command is of no use.
Instead, run:
`python app.py`

### Test Mqtt functionalities
The app subscribes to the "smart_bed" topic of the broker connected to the local 1883 port. (the broker must be running -> see MQTT Broker section)
Having the mosquitto broker and the app running, open a new terminal and navigate to the mosquitto installation folder. There run the command:
`mosquitto_sub -t smart_bed -v`
You now should be able to read the messages published by the app


### Unit tests
To run unit tests, use 
`python -m pytest -v -m "not integrationTest"`

### Integration tests
To run integration tests, use 
`python -m pytest -v -m integrationTest`

To see tests coverage, use
`coverage run -m pytest -v`
`coverage report`
