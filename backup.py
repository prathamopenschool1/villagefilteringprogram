#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
import string
from pprint import pprint
from tkinter import messagebox
from pathlib import Path
import requests


def backup():
    global i, serial_line, res_device, homeDir
    homeDir = str(Path.home())
    homeDir = os.path.join(homeDir, 'generate/Backup')
    print(homeDir)
    deskDir = os.path.join(homeDir, 'DesktopBackup')
    print(deskDir)
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
        # pprint(lstscore)

        headers = {
            'cache-control': "no-cache",
            'content-type': "application/json",
            'Accept': 'application/json'
        }

        # get api
        content_url = 'http://localhost:8080/api/contentsessionlog/?page=%s&page_size=1000' % i
        facility_url = 'http://localhost:8080/api/facilityuser/'
        channel_url = 'http://localhost:8080/api/channel/'
        device_url = 'http://localhost:8080/api/deviceinfo/'

        # post api
        post_url = "http://rpi.prathamskills.org/api/KolibriSession/Post"

        # authentication
        username = "pratham"
        password = "pratham"

        auth = (username, password)

        # content info
        content_response = requests.request("GET", content_url, headers=headers, auth=auth)
        content_result = json.loads(content_response.content.decode("utf-8"))
        # pprint(content_result)

        # print(content_result['next'])
        try:
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            new_data = content_result

            # facility info
            facility_response = requests.request("GET", facility_url, headers=headers, auth=auth)
            facility_result = json.loads(facility_response.content.decode("utf-8"))
            # pprint(facility_result)

            for values in facility_result:
                values["is_superuser"] = ""
                values["collection_parent"] = ""
                # print(values["roles"])
                for collection_parents in values["roles"]:
                    collection_parents["collection_parent"] = ""

            # channel info
            response_channel = requests.request("GET", channel_url, headers=headers, auth=auth)
            res_channel = json.loads(response_channel.content.decode("utf-8"))
            # pprint(res_channel)

            global new_channel_value
            new_channel_value = []

            for datas in res_channel:
                datas["thumbnail"] = ""
                datas["description"] = ""
                datas["available"] = ""

                new_channel_value.append(datas)

            # device info
            try:
                response_device = requests.request("GET", device_url, headers=headers, auth=auth)
                res_device = json.loads(response_device.content.decode("utf-8"))
            except Exception as e:
                messagebox.showinfo("pratham", e)

            # pi id data to be collected
            # os.system('cat /proc/cpuinfo > serial_data.txt')
            # serial_file = open('serial_data.txt', "r+")
            # for line in serial_file:
            #     if line.startswith('Serial'):
            #         serial_line = line  "serial_id": serial_line

            # desktop score data to be posted
            desktop_data_to_post = {
                "channel": new_channel_value,
                "facility_info": facility_result,
                "device_info": res_device,
                "pi_session_info": new_data
            }

            # pprint(desktop_data_to_post)

            try:
                if not os.path.exists(homeDir):
                    os.makedirs(homeDir)
                    if not os.path.exists(deskDir):
                        os.makedirs(deskDir)
                        with open(os.path.join(deskDir,
                                               'dsk'+randstr + str(datetime.datetime.now()) + '.json'),
                                  "w") as outfile:
                            json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                        print(response.status_code, response.reason)
                        pprint(desktop_data_to_post)
                        if response.status_code == 404:
                            return True

                        else:
                            try:
                                with open(os.path.join(homeDir,
                                                       randstr + str(datetime.datetime.now()) + '.json'),
                                          "w") as outfile:
                                    json.dump(lstscore, outfile, indent=4, sort_keys=True)

                            except Exception as e1:
                                messagebox.showinfo("pratham", e1)
                                print(e1)
                                return False

                else:
                    with open(os.path.join(deskDir,
                                           'desk'+randstr + str(datetime.datetime.now()) + '.json'),
                              "w") as outfile:
                        json.dump(desktop_data_to_post, outfile, indent=4, sort_keys=True)
                    print(response.status_code, response.reason)
                    pprint(desktop_data_to_post)
                    if response.status_code == 404:
                        return True

                    else:
                        try:
                            with open(os.path.join(homeDir,
                                                   randstr + str(datetime.datetime.now()) + '.json'),
                                      "w") as outfile:
                                json.dump(lstscore, outfile, indent=4, sort_keys=True)
                                # /opt/PIHDD/KOLIBRI_DATA/content/storage/pdata/Backup

                        except Exception as e1:
                            messagebox.showinfo("pratham", e1)
                            print(e1)
                            return False

            except Exception as e:
                messagebox.showinfo("pratham", e)
                print(e)
                return False

        except Exception as e1:
            messagebox.showinfo("pratham", e1)
            print(e1)
            return False

        if content_result['next'] is None:
            return True

        i = i + 1
