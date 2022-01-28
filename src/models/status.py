from db import get_db
from flask import session
from flask.cli import with_appcontext


class Status:
    __instance = None
   
    selected_mode = None
    future_alarms = None
    height = None
    last_sleep_stats = None
    last_played_song = None
    temperature = None
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
        
        future_alarms = db.execute("select * from alarms where start > DateTime('now') ").fetchall()
        if future_alarms:
            for alarm in future_alarms:
                alarm = dict(zip(alarm.keys(), alarm))
            
        last_played_song = db.execute("select * from songs where active = 1 limit 1").fetchone()
        if last_played_song:
            last_played_song = dict(zip(last_played_song.keys(), last_played_song))
          
        height = db.execute("select * from heights order by timestamp desc limit 1").fetchone()
        if height:
            height = height['value']
          
        last_sleep_stats = db.execute("select * from sleep_stats order by end desc limit 1").fetchone()
        if last_sleep_stats:
            last_sleep_stats = dict(zip(last_sleep_stats.keys(), last_sleep_stats))
          
        temperature = db.execute("SELECT * FROM temperatures ORDER BY TIMESTAMP DESC LIMIT 1").fetchone()
        if temperature:
            temperature = temperature['value']
        
        current_user = db.execute("select * from users where active = 1 limit 1").fetchone()
        if current_user:
            current_user = current_user['id']
          
        return {
            "selected_mode": selected_mode,
            "future_alarms": future_alarms,
            "current_user": current_user,
            "last_played_song": last_played_song,
            "last_sleep_stats": last_sleep_stats,
            "height": height,
            "temperature": temperature
        }
