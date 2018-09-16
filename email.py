import smtplib      '''mailing protocols are smtp based protocols'''
from email.MIMEMultipart import MIMEMultipart       '''multipurpose internet mailing extensions'''
from email.MIMEText import MIMEText
from sense_hat import SenseHat
import time
from time import asctime

sense = SenseHat()      '''establishing communication btw sensehat and program'''

fromaddr="surya.p.4497@gmail.com"
toaddr="imsuryap@hotmail.com"
msg=MIMEMultipart()
msg['From']=fromaddr
msg['To']=toaddr
msg['Subject']="Temp"

temp=round(sense.get_temperature()*1.8+32)
humidity=round(sense.get_humidity())
pressure=round(sense.get_pressure())
message='T=%dF,H=%d,P=%d'%(temp,humidity,pressure)
print(message)
msg.attach(MIMEText(message,'plain'))

server=smtplib.SMTP('smtp.gmail.com',25)       '''standart protocol to access google, standard port 25'''
server.starttls()                              '''starting the server'''
server.login(fromaddr,"password")
text=msg.as_string()                           '''converting the msg into string so that the values go as it is'''
server.sendmail(fromaddr,toaddr,text)
server.quit()