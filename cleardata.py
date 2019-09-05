#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import messagebox
import requests
import json


def clear_data():

    global res_del
    headers = {
        "content-type": "application/json"
    }
    messagebox.showinfo("pratham", "deleting data please wait")
    while True:
        # get request api with pagination
        urls = "http://localhost:8080/pratham/datastore/?page=1&page_size=15"

        # localhost authentication parameters
        username = 'pratham'
        password = 'pratham'

        # getting response from url
        response = requests.get(urls, auth=(username, password))

        # loading response in json format in lstscore variable
        lstscore = json.loads(response.content.decode('utf-8'))

        # checks the value of count
        if lstscore['count'] == 0:
            return True

        else:
            try:
                for obj in lstscore['results']:
                    show_id = obj['id']
                    url_del = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del, headers=headers, auth=(username, password))
                    except Exception as e:
                        messagebox.showinfo("pratham", e)

            except Exception as e1:
                return False

