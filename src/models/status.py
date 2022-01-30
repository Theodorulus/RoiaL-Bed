from db import get_db
from flask import session
from flask.cli import with_appcontext

class Status:
    __instance = None
   
    selected_mode = None
    alarms = []
    height = None
    last_sleep_stats = None
    last_played_song = None
    set_temperature = None
    real_temperature = None
    temperature_status = None
    current_user = None
   
    @staticmethod 
    def getInstance():
        if Status.__instance is None:
            Status()
        return Status.__instance
   
    def __init__(self):
        if Status.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Status.__instance = self
      
    @staticmethod
    def get_status(): 
        db = get_db().cursor()
        
        selected_mode = db.execute("select * from modes where active = 1 limit 1").fetchone()
        if selected_mode:
            selected_mode = selected_mode['id']
        
        db_alarms = db.execute("select * from alarms").fetchall()
        if db_alarms:
            Status.alarms.clear()
            for alarm in db_alarms:
                alarm = dict(zip(alarm.keys(), alarm))
                Status.alarms.append(alarm)
                
        last_played_song = db.execute("select * from songs where active = 1 limit 1").fetchone()
        if last_played_song:
            last_played_song = dict(zip(last_played_song.keys(), last_played_song))
          
        height = db.execute("select * from heights order by timestamp desc limit 1").fetchone()
        if height:
            height = height['value']
          
        last_sleep_stats = db.execute("select * from sleep_stats order by end desc limit 1").fetchone()
        if last_sleep_stats:
            last_sleep_stats = dict(zip(last_sleep_stats.keys(), last_sleep_stats))
          
        set_temperature = db.execute("SELECT * FROM temperatures ORDER BY TIMESTAMP DESC LIMIT 1").fetchone()
        if set_temperature:
            set_temperature = set_temperature['value']
        
        real_temperature = db.execute("SELECT * FROM real_temperatures ORDER BY TIMESTAMP DESC LIMIT 1").fetchone()
        if real_temperature:
            temperature_status = real_temperature['status']
            real_temperature = real_temperature['value']
        
        current_user = db.execute("select * from users where active = 1 limit 1").fetchone()
        if current_user:
            current_user = current_user['id']
          
        return {
            "selected_mode": selected_mode,
            "alarms": Status.alarms,
            "current_user": current_user,
            "last_played_song": last_played_song,
            "last_sleep_stats": last_sleep_stats,
            "height": height,
            "set temperature": set_temperature,
            'real temperature': real_temperature,
            'temperature status': temperature_status
        }
