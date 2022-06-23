import pyfirmata
import smtplib
import datetime

#FOR EMAIL
sender_email="bishal.saha04052002@gmail.com"
rec_email="hanumansaha.1975@gmail.com"
password="pzvohebisqnyxxky"
message="Hey,This is Your Fellow Arduino UNO.I have turned ON Lights,OKKKKK.Arduino UNO..............."

server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(sender_email,password)






#FOR WHATSAPP
import pywhatkit
import time
import pyautogui

import keyboard as k



HOUR = datetime.datetime.now().hour   # the current hour
MINUTE = datetime.datetime.now().minute # the current minute
print(HOUR,MINUTE)

comport='COM5'

board=pyfirmata.Arduino(comport)
led1=board.get_pin('d:12:o')
led2=board.get_pin('d:9:o')




def led(val):
    if val==1:
        led1.write(1)
        led2.write(1)
        print("Hurray It is working.............................................................")
        print("Login Success")
        server.sendmail(sender_email, rec_email, message)
        print("Email has been sent to", rec_email)

    elif val==0:
        led1.write(0)
        led2.write(0)

        pywhatkit.sendwhatmsg('+917585848186','Hey...........,This is Your Fellow Arduino UNO.I have turned OFF Lights,OKKKKK.Arduino UNO...............Automate From Python',HOUR,MINUTE+2 , 30)
        pyautogui.click(1050, 950)

        k.press_and_release('enter')



