import pycurl,json       '''pycurl-establish connection btw API to pass the data'''
from StingIO import StringIO
import RPi.GPIO as GPIO   '''general input output from raspberry pi'''
from sense_hat import SenseHat
import time
from time import asctime

sense = SenseHat()
sense.clear()            '''clears the previous data'''

cold=37
hot=40
pushMessage=""


#Code for display number

OFFSET_LEFT=1
OFFSET_TOP=2

NUMS=[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  #0
      0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  #1
	  1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  #2
	  1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  #3
	  1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  #4
	  1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  #5
	  1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  #6
	  1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  #7
	  1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  #8
	  1,1,1,1,0,1,1,1,1,0,0,1,0,0,1,] #9
	  
#Display of single digit(0-9)
def show_digit(val,xd,yd,r,g,b):
  offset=val*15
  for p in range(offset,offset+15):
    xt=p%3
    yt=(p-offset)//3
    sense.set_pixel(xt+xd,yt+yd,r*NUMS[p],g*NUMS[p],b*NUMS[p])

#Display of two digit(0-9)
def show_number(val,r,g,b):
  abs_val=abs(val)
  tens=abs_val//10
  units=abs_val%10
  if(abs_val>9): 
   show_digit(tens,OFFSET_LEFT,OFFSET_TOP,r,g,b)
   show_digit(units,OFFSET_LEFT+4,OFFSET_TOP,r,g,b)
   

temp=round(sense.get_temperature())
humidity=round(sense.get_humidity())
pressure=round(sense.get_pressure())
message='T=%dC,H=%d,P=%d'%(temp,humidity,pressure)

#setup of InstaPush variables
#adding InstaPush Application ID
appID="5b9dfc131db2dc4d7c345889"

#adding InstaPush Application Secret
appSecret="50b2fe03e1378133bd080095b8558b91"
pushEvent="weather"

#usng curl to post to instapush api
c=pycurl.Curl()

#seting API URL
c.setup(c.URL,'https://api.instapush.im/post')

#setup of custom headers for authentication variables and content type
c.setup(c.HTTPHEADER,['x-instapush-appid:'+appID,'x-instapush-appSecret:'+appSecret,'Content-Type:application/json'])

#capturing response from push API call
buffer=StingIO()


def p(pushMessage):
    #creating a dict structure for the JSON data to post
	json_fields={}
	
	#setting json values
	json_fields['event']=pushEvent
	json_fields['trackers']={}
	json_fields['trackers']['message']=pushMessage
	print(json_fields)
	postfields=json.dumps(json_fields)
	
	#sending json with post
	c.setopt(c.POSTFIELDS,postfields)
	
	#capturing response in the buffer
	c.setopt(c.WRITEFUNCTION,buffer.write)
	
	#check for post sent
	c.setopt(c.VERBOSE,True)
	
#setting an indefinite loop that looks for temp
while True:
    temp=round(sense.get_temperature())
    humidity=round(sense.get_humidity())
    pressure=round(sense.get_pressure())
    message='T=%dC,H=%d,P=%d'%(temp,humidity,pressure)
	time.sleep(4)
	log=open('weather.txt',"a")
	now=str(asctime())
	temp=int(temp)
	show_number(temp,200,0,60)
	temp1=temp
	
	log.write(now+''+message+'\n')
	print(message)
	log.close()
	time.sleep(5)
	
	if temp>=hot:
	     pushMessage="hot:"+message
		 p(pushMessage)
		 c.perform()
		 #capturing response from server
		 body=buffer.getvalue()
		 pushMessage=""
		 
	elif temp<=cold:
	     pushMessage="cold:"+message
		 p(pushMessage)
		 #capturing response from server
		 body=buffer.getvalue()
		 pushMessage=""
		 
	#printing the response
	print(body)
	
	#reset buffer
	buffer.truncate(0)
	buffer.seek(0)
	
#cleanup
c.close()
GPIO.cleanup()	
	
	


