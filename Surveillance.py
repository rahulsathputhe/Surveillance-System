import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
import RPi.GPIO as GPIO
import urllib2
import cookielib
from getpass import getpass
import sys
from stat import *

def measure():
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()

  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average():
  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance


def sendNotification(message, number):
    #message = "HII HELLO"
    #number = "9494267335"
    username = "9494267335"
    passwd = "9964"

    message = "+".join(message.split(' '))

    #logging into the sms site
    url ='http://site24.way2sms.com/Login1.action?'
    data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

    #For cookies

    cj= cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    #Adding header details
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
    try:
        usock =opener.open(url, data)
    except IOError:
        print "error"
        #return()

    jession_id =str(cj).split('~')[1].split(' ')[0]
    send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
    opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
    try:
        sms_sent_page = opener.open(send_sms_url,send_sms_data)
    except IOError:
        print "error"
        #return()

    print "success" 
    #return ()

def send_email(iM,s):

        fromaddr = 'rahulsathputhe7@gmail.com'
        toaddrs=str(iM)
        msg = MIMEMultipart()

        text = MIMEText(str(s))
        msg['Subject'] = 'Surveillance System'
        msg.attach(text)
        img_data = open('picture.jpg', 'rb').read()
        image = MIMEImage(img_data, name='picture.jpg')
        msg.attach(image)

        # Credentials (if needed)
        username = 'rahulsathputhe7@gmail.com'
        password = 'rahul9964'

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
        print('e-Mail Sent')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_TRIGGER = 23
GPIO_ECHO    = 24

print "Ultrasonic Measurement"

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  
GPIO.setup(GPIO_ECHO,GPIO.IN)      

GPIO.output(GPIO_TRIGGER, False)


try:

  while True:

    distance = measure_average()
    print "Distance : %.1f cm" % distance
    if(distance<60):
        
        
	sendNotification('Intruder Detected','9494267335')
	os.system('./webcam.sh')
	send_email('rahulsathputhe@gmail.com','Intrusion Detection')
    

    time.sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()

