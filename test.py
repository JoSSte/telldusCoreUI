import time
import random
import callbackService

for x in range(10):
  callbackService.sensor_event( '', '', '999', 'temperature', random.randint(-2900, -190)/10, int(time.time()), '-666')
  time.sleep(1)