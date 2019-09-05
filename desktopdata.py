#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint
import os
from tkinter import messagebox

import requests
import json


def get_new_data():

    global i, serial_line
    serial_line = ''
    i = 1

    messagebox.showinfo("pratham", "wait while data is posting")

    while True:

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

            for values in facility_result:
                values["is_superuser"] = ""
                values["collection_parent"] = ""
                # print(values["roles"])
                for collection_parents in values["roles"]:
                    collection_parents["collection_parent"] = ""

            # channel info
            response_channel = requests.request("GET", channel_url, headers=headers, auth=auth)
            res_channel = json.loads(response_channel.content.decode("utf-8"))

            global new_channel_value
            new_channel_value = []

            for datas in res_channel:
                datas["thumbnail"] = ""
                datas["description"] = ""
                datas["available"] = ""

                new_channel_value.append(datas)

            # device info
            response_device = requests.request("GET", device_url, headers=headers, auth=auth)
            res_device = json.loads(response_device.content.decode("utf-8"))

            # pi id data to be collected
            os.system('cat /proc/cpuinfo > serial_data.txt')
            serial_file = open('serial_data.txt', "r+")
            for line in serial_file:
                if line.startswith('Serial'):
                    serial_line = line

            # print(serial_line)

            # desktop score data to be posted
            desktop_data_to_post = {
                "channel": new_channel_value,
                "facility_info": facility_result,
                "device_info": res_device,
                "pi_session_info": new_data,
                "serial_id": serial_line
            }

            try:
                response_post = requests.post(
                    post_url,
                    headers=headers,
                    data=json.dumps(desktop_data_to_post),
                    auth=(username, password)
                )
                # print(response_post.status_code, response_post.reason)
                # pprint(desktop_data_to_post)

            except Exception as e:
                return False

        except Exception as e:
            return False

        if content_result['next'] is None:
            return True

        i = i + 1

# get_new_data()
