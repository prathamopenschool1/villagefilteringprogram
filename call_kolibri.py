#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pprint import pprint
from tkinter import messagebox
import requests
import json
import os
import datetime
import string
import random


def call_kolbri():

    global res_del, i, serial_line
    i = 1
    n = 6
    serial_line = ''
    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    messagebox.showinfo("pratham", "wait for few minutes while data is posting")

    while True:
        # get request api with pagination
        urls = "http://localhost:8080/pratham/datastore/?table_name=USAGEDATA&page=%s&page_size=15" % i

        # post api
        url = "http://www.rpi.prathamskills.org/api/pushdata/post/"
        # url = "http://pratham.openiscool.org/api/pushdata/post/"params={'page': page}

        # localhost authentication parameters
        username = 'pratham'
        password = 'pratham'

        # getting response from url
        response = requests.get(urls, auth=(username, password))

        # loading response in json format in lstscore variable
        lstscore = json.loads(response.content.decode('utf-8'))
        # pprint(lstscore)

        # pi id data to be collected
        os.system('cat /proc/cpuinfo > serial_data.txt')
        serial_file = open('serial_data.txt', "r+")
        for line in serial_file:
            if line.startswith('Serial'):
                serial_line = line

        lstscore['serial_id'] = serial_line

        # checks the value of count
        if lstscore['count'] == 0:
            return True

        # posting data to different post server
        else:

            headers = {
                "content-type": "application/json"
            }
            data = lstscore  # providing lstscore value to data variable

            try:
                response_post = requests.post(
                    url,
                    headers=headers,
                    data=json.dumps(data),
                    auth=(username, password)
                )
                # print(response_post.status_code, response_post.reason)

                if response_post.status_code == 200:

                    for obj in lstscore['results']:
                        show_id = obj['id']
                        url_del = "http://localhost:8080/pratham/datastore/" + show_id
                        try:
                            res_del = requests.delete(url_del, headers=headers, auth=(username, password))
                        except Exception as e:
                            return False
                            # messagebox.showinfo("pratham", e)

                    try:
                        with open(os.path.join("/opt/PIHDD/KOLIBRI_DATA/content/storage/pdata/Backup",
                                               randstr + str(datetime.datetime.now()) + '.json'),
                                  "w") as outfile:
                            json.dump(lstscore, outfile, indent=4, sort_keys=True)
                            # /opt/PIHDD/KOLIBRI_DATA/content/storage/pdata/Backup
                    except Exception as e2:
                        messagebox.showinfo("pratham", e2)



                else:
                    return False

            except Exception as e1:
                return False
