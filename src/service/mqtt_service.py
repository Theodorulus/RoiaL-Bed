from src.service.temperature_service import update_realtime_temperature


# Here should be included all the functions that must be called by mqtt to update the database every second
def update_database_mqtt():
    update_realtime_temperature()
