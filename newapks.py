import requests
import os
from tkinter import messagebox


def update_tab_apk():
    os.system('sudo chmod 777 -R /var/www/html/data/')
    messagebox.showinfo("pratham", "wait while apk is being updated")

    tab_url = "http://rpi.prathamskills.org/apps/TabPraDigi.apk"  # TabPraDigi.apk

    apk_tab = requests.get(tab_url, stream=True)

    with open("/var/www/html/data/TabPraDigi.apk", 'wb') as f:
        f.write(apk_tab.content)


def update_smart_apk():
    update_tab_apk()
    smart_url = "http://rpi.prathamskills.org/apps/SmartPhonePraDigi.apk"  # SmartPhonePraDigi.apk

    apk_smart = requests.get(smart_url, stream=True)

    with open('/var/www/html/data/SmartPhonePraDigi.apk', 'wb') as smart:
        smart.write(apk_smart.content)

    if apk_smart.status_code == 200:
        return True
    else:
        return False

