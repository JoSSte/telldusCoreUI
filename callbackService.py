#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import sqlite3
import tellcore.telldus as td
import tellcore.constants as const
import os
from datetime import date, datetime, timedelta
from mysql.connector import errorcode
from dotenv import load_dotenv

from sqlite3 import Error

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')
SQLITE_DB = 'localcache.db'
DEBUG=os.getenv('DEBUG')


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

def cache_data(protocol, model, id_, dataType, value, timestamp, cid):
  conn1 = sqlite3.connect(SQLITE_DB)
  cur1 = conn1.cursor()
  print('caching. . . ', end='')
  try:
    cur1.execute("INSERT INTO sensorData (sensorid, timestamp, value, valuetype) values (?,?,?,?)", (id_, timestamp, value, dataType))
    conn1.commit()
    print('cached. . .  ', end='')
  except Error as e:
    print("Error caching %s" % (' '.join(e.args)))
  else:
    conn1.close()
  
# called only if database is there
def check_cache():
  if DEBUG:
    print("Checking if there are cached entries")
  conn2 = sqlite3.connect(SQLITE_DB)
  cur2 = conn2.cursor()
  error_encountered = False
  try:
    cur2.execute("SELECT sensorid, valuetype, value, timestamp FROM sensorData")
    rows = cur2.fetchall()
    conn2.close()
    if DEBUG:
      print("Found %d cached entries" % (len(rows)))
    for row in rows:
      ret = sensor_event('', '', row[0], row[1], row[2], row[3], '', False)
      # abort if database goes away
      if ret <0:
        error_encountered = True
        break
      else:
        print("deleting entry %s %s %s %s " % (row[0], row[1], row[2], row[3]))
        #delete_cache_entry('', '', row[0], row[1], row[2], row[3], '')
    if not error_encountered and len(rows) > 0:
      delete_cache_entries()
  except Error as e:
    print("Error handling cache %s" % (' '.join(e.args)))
  else:
    conn2.close()

def delete_cache_entry(protocol, model, id_, dataType, value, timestamp, cid):
  conn3 = sqlite3.connect(SQLITE_DB)
  cur3 = conn3.cursor()
  try:
    cur3.execute("DELETE FROM sensorData WHERE sensorid =? AND valuetype =? AND value =? AND timestamp =?", (id_, timestamp, value, dataType))
    conn3.commit()
  except Error as e:
    print("Error Deleting cache entry %s" % (' '.join(e.args)))
  else:
    conn3.close()
    print("deleted")

def delete_cache_entries():
  conn3 = sqlite3.connect(SQLITE_DB)
  cur3 = conn3.cursor()
  try:
    cur3.execute("DELETE FROM sensorData")
    conn3.commit()
  except Error as e:
    print("Error deleting cache entries:  %s" % (' '.join(e.args)))
  else:
    conn3.close()
    print("Cache cleared")

# Callback handler Sensor Event
def sensor_event(protocol, model, id_, dataType, value, timestamp, cid, cache_enable=True):
  #print("Sensorevent (protocol: %s, model: %s, id_: %s, dataType: %s, value: %s, timestamp: %s, cid: %s)"%(protocol, model, id_, dataType, value, timestamp, cid))
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
    if cache_enable:
        check_cache()
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name (%s) or password. Caching data for later. . . " % (MYSQL_USER), end='')
      if cache_enable:
        cache_data(protocol, model, id_, dataType, value, timestamp, cid)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database %s does not exist on host %s. Caching data for later. . . " % (MYSQL_DB, MYSQL_HOST), end='')
      if cache_enable:
        cache_data(protocol, model, id_, dataType, value, timestamp, cid)
    elif err.errno == errorcode.CR_CONN_HOST_ERROR:
      print("Connection Issue: %s - potential network error. Caching data for later. . . " % (err.msg), end='')
      if cache_enable:
        cache_data(protocol, model, id_, dataType, value, timestamp, cid)
    else:
      print(err)
    return -1
  else:
    cursor.close()
    cnx.close()
  # output of '..' means it went well
  print('.')
  return 0

# Callback handler Button Event
def device_event(id_, method, data, cid):
    method_string = METHODS.get(method, "UNKNOWN METHOD {0}".format(method))
    string = "[DEVICE] {0} -> {1}".format(id_, method_string)
    if method == const.TELLSTICK_DIM:
        string += " [{0}]".format(data)
    print(string)

if not DEBUG:
  # Callback handling
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
