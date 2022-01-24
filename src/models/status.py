from db import get_db
from flask import session
from flask.cli import with_appcontext

class Status():
    __instance = None
   
    selectedMode = None
    futureAlarms = None
    height = None
    lastSleepStats = None
    lastPlayedSong = None
    temperature = None
    currentUser = None
   
    @staticmethod 
    def getInstance():
      if Status.__instance == None:
         Status()
      return Status.__instance
   
    def __init__(self):
      if Status.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Status.__instance = self
      
    @staticmethod
    def get_status(): 
        db= get_db().cursor()
        
        selectedMode = db.execute("select * from modes where active == 1 limit 1" ).fetchone()
        if selectedMode:
          selectedMode = selectedMode['id']
        
        futureAlarms = db.execute("select * from alarms where start > DateTime('now') ").fetchall()
        if futureAlarms:
          for alarm in futureAlarms:
            alarm = dict(zip(alarm.keys(), alarm))
            
        lastPlayedSong = db.execute("select * from songs where active == 1 limit 1" ).fetchone()
        if lastPlayedSong:
          lastPlayedSong = dict(zip(lastPlayedSong.keys(), lastPlayedSong))
          
        height = db.execute("select * from heights order by timestamp desc limit 1" ).fetchone()
        if height:
          height = height['value']
          
        lastSleepStats = db.execute("select * from sleep_stats order by end desc limit 1" ).fetchone()
        if lastSleepStats:
          lastSleepStats = dict(zip(lastSleepStats.keys(), lastSleepStats))
          
        temperature = db.execute("SELECT * FROM temperatures ORDER BY TIMESTAMP DESC LIMIT 1").fetchone()
        if temperature:
          temperature = temperature['value']        
        
        currentUser = db.execute("select * from users where active = 1 limit 1" ).fetchone()
        if currentUser:
          currentUser = currentUser['id']
          
        return {
            "selectedMode": selectedMode,
            "futureAlarms": futureAlarms,
            "currentUser": currentUser,
            "lastPlayedSong": lastPlayedSong,
            "lastSleepStats": lastSleepStats,
            "height": height,
            "temperature": temperature
        }
        