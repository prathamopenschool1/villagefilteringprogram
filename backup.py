#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
import string
from tkinter import messagebox

import requests


def backup():

    global i
    i = 1
    n = 6
    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    messagebox.showinfo("pratham", "wait for sometime while we take backup")

    while True:
        # get request api with pagination
        urls = "http://localhost:8080/pratham/datastore/?table_name=USAGEDATA&page=%s&page_size=15" % i

        # localhost authentication parameters
        username = 'pratham'
        password = 'pratham'

        # getting response from url
        response = requests.get(urls, auth=(username, password))

        # loading response in json format in lstscore variable
        lstscore = json.loads(response.content.decode('utf-8'))

        # print(response.status_code, i)

        if response.status_code == 404:
            return True

        else:
            try:
                with open(os.path.join("/opt/PIHDD/KOLIBRI_DATA/content/storage/pdata/Backup",
                                       randstr + str(datetime.datetime.now()) + '.json'),
                          "w") as outfile:
                    json.dump(lstscore, outfile, indent=4, sort_keys=True)
                    # /opt/PIHDD/KOLIBRI_DATA/content/storage/pdata/Backup

            except Exception as e1:
                return False

        i = i+1

