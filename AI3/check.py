import webbrowser as web
import time
import keyword




b='close the door'
c='madhu'
if c=='basudeb':
    open_chat = "https://web.whatsapp.com/send?phone=+91 7585848186 &text="+str(b)
    web.open(open_chat)
    keyword.press('enter')

elif c=='madhu':
    open_chat = "https://web.whatsapp.com/send?phone=+91 75858 48226 &text=" + str(b)
    web.open(open_chat)
    keyword.press('enter')
