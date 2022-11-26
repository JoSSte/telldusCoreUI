import time
import random
import callbackService

# remember to set DEBUG=True in .env

for x in range(10):
  callbackService.sensor_event( '', '', '999', 'temperature', random.randint(-2900, -190)/10, int(time.time()), '-666')
  time.sleep(1)