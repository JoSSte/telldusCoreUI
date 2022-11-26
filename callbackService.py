#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import tellcore.telldus as td
import tellcore.constants as const
import os
from datetime import date, datetime, timedelta
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')
SQLITE_DB = 'localcache.db'


# initialize SQlite database for local cache
conn = sqlite3.connect(SQLITE_DB)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS sensorData (
  sensorid int(11) DEFAULT NULL,
  timestamp datetime DEFAULT NULL,
  value float DEFAULT NULL,
  valuetype TEXT CHECK( valuetype IN ('temperature','humidity') ) DEFAULT NULL
)
""")
conn.close()

def cache_data(protocol, model, id_, dataType, value, timestamp, cid):
  conn = sqlite3.connect(SQLITE_DB)
  c = conn.cursor()
  print('caching. . . ', end='')
  try:
    c.execute("INSERT INTO sensorData (sensorid, timestamp, value, valuetype) values (?,?,?,?)", (id_, timestamp, value, dataType))
    conn.commit()
    print('cached. . .  ', end='')
  except Error as e:
    print("Error caching " + e)
  else:
    conn.close()

METHODS = {const.TELLSTICK_TURNON: 'turn on',
           const.TELLSTICK_TURNOFF: 'turn off',
           const.TELLSTICK_BELL: 'bell',
           const.TELLSTICK_TOGGLE: 'toggle',
           const.TELLSTICK_DIM: 'dim',
           const.TELLSTICK_LEARN: 'learn',
           const.TELLSTICK_EXECUTE: 'execute',
           const.TELLSTICK_UP: 'up',
           const.TELLSTICK_DOWN: 'down',
           const.TELLSTICK_STOP: 'stop'}

#Callback handler Sensor Event

def sensor_event(protocol, model, id_, dataType, value, timestamp, cid):
  try:
    # output of '..' means it went well
    print('.', end='')
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,host=MYSQL_HOST,database=MYSQL_DB)
    cursor = cnx.cursor()
    add_temperature = ("INSERT INTO sensorData (sensorid, timestamp, value, valuetype) values (%s,from_unixtime(%s),%s,%s)")
    data_temperature = (id_, timestamp, value, dataType)

    #Insert temperature data
    cursor.execute(add_temperature, data_temperature)
    cnx.commit()
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name (%s) or password. Caching data for later. . . " % (MYSQL_USER), end='')
      cache_data(protocol, model, id_, dataType, value, timestamp, cid)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database %s does not exist on host %s. Caching data for later. . . " % (MYSQL_DB, MYSQL_HOST), end='')
      cache_data(protocol, model, id_, dataType, value, timestamp, cid)
    elif err.errno == errorcode.CR_CONN_HOST_ERROR:
      print("Connection Issue: %s - potential network error. Caching data for later. . . " % (err.msg), end='')
      cache_data(protocol, model, id_, dataType, value, timestamp, cid)
  else:
    cursor.close()
    cnx.close()
  # output of '..' means it went well
  print('.')

#Callback handler Button Event
def device_event(id_, method, data, cid):
    method_string = METHODS.get(method, "UNKNOWN METHOD {0}".format(method))
    string = "[DEVICE] {0} -> {1}".format(id_, method_string)
    if method == const.TELLSTICK_DIM:
        string += " [{0}]".format(data)
    print(string)

#Callback handling
try:
    import asyncio
    loop = asyncio.get_event_loop()
    dispatcher = td.AsyncioCallbackDispatcher(loop)
except ImportError:
    loop = None
    dispatcher = td.QueuedCallbackDispatcher()

core = td.TelldusCore(callback_dispatcher=dispatcher)
callbacks = []

#register callback for sensor event
callbacks.append(core.register_sensor_event(sensor_event))
callbacks.append(core.register_device_event(device_event))

#Handle events
try:
    if loop:
        loop.run_forever()
    else:
        import time
        while True:
            core.callback_dispatcher.process_pending_callbacks()
            time.sleep(0.5)
            print('-')
except KeyboardInterrupt:
    pass
