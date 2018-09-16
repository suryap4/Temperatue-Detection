from sense_hat import SenseHat
import time
from time import asctime

sense = SenseHat()

while True:
  temp=round(sense.get_temperature()*1.8+32)
  humidity=round(sense.get_humidity())
  pressure=round(sense.get_pressure())
  message='T=%dF,H=%d,P=%d'%(temp,humidity,pressure)
  sense.show_message(message,scroll_speed=(0.06),text_colour=[200,240,200],back_colour=[0,0,0]
  time.sleep(4)
  log=open('weather.txt,"a")
  now=str(asctime())
  log.write(now+''+message+'\n')        '''saves measured values in text file'''
  print(message)
  log.close()
  time.sleep(5) 
