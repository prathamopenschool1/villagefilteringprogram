#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from tkinter import messagebox

import requests


def check_internet():
    url_check = 'http://www.hlearning.openiscool.org/api/crl/get/'
    timeout = 3
    try:
        _ = requests.get(url_check, timeout=timeout)
        return True
    except requests.ConnectionError:
        messagebox.showinfo("pratham", "please check your internet connection")
        sys.exit(0)

