from src.service.temperature_service import update_realtime_temperature


# All the functions that must be called by mqtt to update the database every second should be included here
def update_database_mqtt():
    update_realtime_temperature()
