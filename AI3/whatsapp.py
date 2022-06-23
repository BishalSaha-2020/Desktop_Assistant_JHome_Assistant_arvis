import webbrowser as web
import time
import keyword

def whatsapp(no,me):
    n= '+91'+int(no)
    m=me
    open_chat="https://web.whatsapp.com/send?photo="
    web.open(open_chat)

    keyword.press('enter')

