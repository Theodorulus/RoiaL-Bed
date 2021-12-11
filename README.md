# RoiaL-Bed

### Requirements:
-1) Install museqito Mqtt broker, if you do not have one already, following: http://www.steves-internet-guide.com/install-mosquitto-broker/
Note: To run the mosquitto broker, you must enter `mosquitto` command in terminal at the mosquitto installation folder (by default being "C:\Program files\mosquitto")
-2) Install app dependencies
Run: 
`pip install -r dependencies.txt`

### Running the app:
Because flask-mqtt cannot run multiple workers(threads) at the same time, and because the app has a main HTTP thread and another one for Mqtt, `flask run` command is of no use.
Instead, run:
`python app.py`

### Test Mqtt functionalities
The app subscribes to the "smart_bed" topic of the broker connected to the local 1883 port.
Having the mosquitto broker and the app running, open a new terminal and navigate to the mosquitto installation folder. There run the command:
`mosquitto_sub -t smart_bed -v`
You now should be able to read the messages published by the app