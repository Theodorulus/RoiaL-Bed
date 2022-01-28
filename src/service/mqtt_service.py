from src.service.temperature_service import set_temperature_realtime


# Here should be included all the functions that must be called by mqtt to update the database every second
def update_database_mqtt():
    set_temperature_realtime()
