#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import ttk
from call_kolibri import call_kolbri
from backup import backup
from live import *
from check import check_internet
from cleardata import clear_data
from newapks import update_smart_apk
from desktopdata import get_new_data
from tkinter import messagebox
import requests
import json
import sys

if sys.version_info[0] >= 3:
    import tkinter as tk
else:
    import Tkinter as tk

LARGE_FONT = ("Verdana", 12)


class CrlUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "PKAPP")

        container = tk.Frame(self)
        container.pack(anchor=tk.CENTER, fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for pages in (StartPage, ProgramState):
            frame = pages(container, self)
            self.frames[pages] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        tk.Frame.__init__(self, parent)

        def push_data():
            check_internet()
            retcallkolibri = call_kolbri()
            if retcallkolibri:
                messagebox.showinfo("pratham", "data post completed!")
            else:
                messagebox.showinfo("pratham", "some problem occurred!")

        def backup_data():
            bk = backup()
            if bk:
                messagebox.showinfo("pratham", "data backup completed!")
            else:
                messagebox.showinfo("pratham", "some problem occurred!")

        def look_internet():
            check_internet()
            controller.show_frame(ProgramState)

        def delete_data():
            cl = clear_data()
            if cl:
                messagebox.showinfo("pratham", "data deleted")
            else:
                messagebox.showinfo("pratham", "some problem occurred!")

        def update_apks():
            check_internet()
            retupdateapk = update_smart_apk()
            if retupdateapk:
                messagebox.showinfo("pratham", "Apks has been updated")
            else:
                messagebox.showinfo("pratham", "please check internet connection")

        def desktop_data():
            check_internet()
            retdeskdata = get_new_data()
            if retdeskdata:
                messagebox.showinfo("pratham", "data post completed!")
            else:
                messagebox.showinfo("pratham", "some problem occurred!")

        pull = ttk.Button(self, text="PULL DATA", command=look_internet, width=12)
        pull.grid(sticky="W", row=5, column=0, padx=2, pady=120)
        push = ttk.Button(self, text="PUSH DATA", command=push_data, width=13)
        push.grid(sticky="W", row=5, column=2, padx=2, pady=120)
        back_up = ttk.Button(self, text="BACKUP DATA", command=backup_data, width=12)
        back_up.grid(sticky="W", row=5, column=4, padx=2, pady=120)
        call_apk = ttk.Button(self, text="UPDATE APK", command=update_apks, width=12)
        call_apk.grid(sticky="W", row=7, column=0, padx=2, pady=30)
        desk = ttk.Button(self, text="DESKTOP DATA", command=desktop_data, width=13)
        desk.grid(sticky="W", row=7, column=2, padx=2, pady=30)
        clear = ttk.Button(self, text="DELETE DATA", command=delete_data, width=12)
        clear.grid(sticky='W', row=7, column=4, padx=2, pady=30)


class ProgramState(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        try:
            c = LiveCall()
            self.programlist = c.getprogramlist()

            # programs dropdown
            self.program = tk.StringVar(self)

            self.programs_menu = tk.OptionMenu(self, self.program, *self.programlist,
                                               command=lambda x: self.programchange(x))
            tk.Label(self, text="Choose a program").grid(row=2, column=0, padx=110, pady=5)
            self.programs_menu.grid(row=3, column=0, padx=110, pady=5)

            label = ttk.Label(self, text="", font=LARGE_FONT)
            label.grid(row=0, column=0)
        except Exception as e:
            pass

    def programchange(self, chosen):

        try:
            self.states_menu.destroy()
        except Exception as e:
            print(e)

        try:
            c = LiveCall()
            self.stateList = c.getstatelist(self.programlist[self.program.get()])
            self.states = tk.StringVar(self)

            self.states_menu = tk.OptionMenu(self, self.states, *self.stateList, command=lambda x: self.getdistricts(x))
            tk.Label(self, text="Choose a state").grid(row=4, column=0, padx=110, pady=5)
            self.states_menu.grid(row=5, column=0, padx=110, pady=5)
        except Exception as e:
            messagebox.showinfo("PKAPP", e)

    def getstates(self):
        try:
            c = LiveCall()
            c.crl_call(p=str(self.programlist[self.program.get()]), s=self.stateList[self.states.get()])
        except Exception as e:
            print(e)

    def getdistricts(self, choose):
        try:
            self.district_menu.destroy()
        except Exception as e:
            print(e)

        try:
            c = LiveCall()

            # district data
            self.district_list = c.district_call(p=str(self.programlist[self.program.get()]),
                                                 s=self.stateList[self.states.get()])

            self.districts = tk.StringVar(self)
            self.district_menu = tk.OptionMenu(self, self.districts, *self.district_list,
                                               command=lambda x: self.getblocks(x))
            tk.Label(self, text="Choose your district").grid(row=6, column=0, padx=110, pady=5)
            self.district_menu.grid(row=7, column=0, padx=110, pady=5)
            self.district_list1 = c.district_lists

        except Exception as e:
            messagebox.showinfo("PKAPP", e)

    def getblocks(self, choose):
        try:
            self.blocks_menu.destroy()
        except Exception as e1:
            print(e1)

        try:
            c = LiveCall()

            # blocks data
            self.blocks_list = c.block_call(p=str(self.programlist[self.program.get()]),
                                            s=self.stateList[self.states.get()],
                                            d=self.districts.get())

            self.blocks = tk.StringVar(self)
            self.blocks_menu = tk.OptionMenu(self, self.blocks, *self.blocks_list)
            tk.Label(self, text="Choose your block").grid(row=9, column=0, padx=110, pady=5)
            self.blocks_menu.grid(row=10, column=0, padx=110, pady=5)
            ok = ttk.Button(self, text="OK", command=self.create_new_window, width=5)
            ok.grid(row=12, column=0)

        except Exception as e1:
            messagebox.showinfo("PKAPP", e1)

    def getvillages(self):
        try:
            c = LiveCall()
            self.my_village_list = c.villages_call(p=str(self.programlist[self.program.get()]),
                                                   s=self.stateList[self.states.get()], b=self.blocks.get())
            self.allvillagelist = c.allvillage_call()
            self.villages = c.myvillagelist
        except Exception as e:
            messagebox.showinfo("PKAPP", e)

    def create_new_window(self):
        try:
            if self.districts.get():
                self.getvillages()
                t = tk.Toplevel(self)
                t.wm_title("PKAPP")

                # Gets the requested values of the height and width.
                windowWidth = t.winfo_reqwidth()
                windowHeight = t.winfo_reqheight()

                # Gets both half the screen width/height and window width/height
                positionRight = int(t.winfo_screenwidth() / 8 - windowWidth / 2)
                positionDown = int(t.winfo_screenheight() / 2 - windowHeight / 3)

                # Positions the window in the center of the page.
                t.geometry("+{}+{}".format(positionRight, positionDown))

                row, column = 2, 0

                self.checkbox_value = []

                self.prog_name = tk.Label(t, text="Program: %s" % self.program.get()).grid(sticky="W", row=0,
                                                                                           column=0, padx=2, pady=2)
                self.state_name = tk.Label(t, text="State: %s" % self.states.get()).grid(sticky="W", row=0,
                                                                                         column=1, padx=2, pady=2)
                self.block_name = tk.Label(t, text="Block: %s" % self.blocks.get()).grid(sticky="W", row=0,
                                                                                         column=2, padx=2, pady=2)
                self.ok = ttk.Button(t, text="OK", width=5, command=self.selected).grid(sticky="W", row=0,
                                                                                        column=4, padx=2, pady=2)
                self.close = ttk.Button(t, text="close", width=5, command=t.destroy).grid(sticky="W", row=0,
                                                                                          column=5, padx=2, pady=2)

                self.send_village = []

                self.var = {}
                self.var.clear()
                for item in self.villages:
                    self.var[item] = tk.IntVar()
                    self.check_button = tk.Checkbutton(t, text=item, variable=self.var[item])
                    self.check_button.grid(sticky="W", row=row, column=column, padx=2, pady=2)

                    row = row + 1
                    if row > 17:
                        row = 2
                        column = column + 1
            else:
                messagebox.showinfo("PKAPP", "Problem occurred while loading please check internet connection")
        except Exception as e:
            messagebox.showinfo("PKAPP", e)

    def selected(self):
        c = LiveCall()
        messagebox.showinfo("PKAPP", "wait while data is downloading")
        try:
            self.send_village = []
            for key, value in self.var.items():
                if value.get() > 0:
                    self.send_village.append(key)

            # print(self.var)
            self.getstates()
            c.postvillage(p=str(self.programlist[self.program.get()]),
                          s=self.stateList[self.states.get()], b=self.blocks.get(),
                          av=self.allvillagelist, v=self.send_village)
        except Exception as e:
            messagebox.showinfo("PKAPP", e)

        try:
            hindi_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_Hindi.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            hindi_response_data = requests.request("GET", hindi_url, headers=headers)
            hindi_result_data = json.loads(hindi_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Hindi"

            hindi_payload = {"data": hindi_result_data, "filter_name": filter_name, "table_name": table_name,
                             "facility": self.facility}
            hindi_payload1 = json.dumps(hindi_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                hindi_response_post = requests.request("POST",
                                                       sawaal_post_url,
                                                       data=hindi_payload1,
                                                       headers=headers,
                                                       auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as ex:
            messagebox.showinfo("PKAPP", ex)

        try:
            marathi_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_Marathi.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            marathi_response_data = requests.request("GET", marathi_url, headers=headers)
            marathi_result_data = json.loads(marathi_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Marathi"

            marathi_payload = {"data": marathi_result_data, "filter_name": filter_name, "table_name": table_name,
                               "facility": self.facility}
            marathi_payload1 = json.dumps(marathi_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                marathi_response_post = requests.request("POST",
                                                         sawaal_post_url,
                                                         data=marathi_payload1,
                                                         headers=headers,
                                                         auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as ex:
            messagebox.showinfo("PKAPP", ex)

        try:
            bengali_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_BENGALI.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            bengali_response_data = requests.request("GET", bengali_url, headers=headers)
            bengali_result_data = json.loads(bengali_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Bengali"

            bengali_payload = {"data": bengali_result_data, "filter_name": filter_name, "table_name": table_name,
                               "facility": self.facility}
            bengali_payload1 = json.dumps(bengali_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                bengali_response_post = requests.request("POST",
                                                         sawaal_post_url,
                                                         data=bengali_payload1,
                                                         headers=headers,
                                                         auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as ex:
            messagebox.showinfo("PKAPP", ex)

        try:
            assamese_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_ASSAMESE.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            assamese_response_data = requests.request("GET", assamese_url, headers=headers)
            assamese_result_data = json.loads(assamese_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Assamese"

            assamese_payload = {"data": assamese_result_data, "filter_name": filter_name, "table_name": table_name,
                                "facility": self.facility}
            assamese_payload1 = json.dumps(assamese_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                assamese_response_post = requests.request("POST",
                                                          sawaal_post_url,
                                                          data=assamese_payload1,
                                                          headers=headers,
                                                          auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as ex:
            messagebox.showinfo("PKAPP", ex)

        try:
            oriya_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_ORIYA.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            oriya_response_data = requests.request("GET", oriya_url, headers=headers)
            oriya_result_data = json.loads(oriya_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Oriya"

            oriya_payload = {"data": oriya_result_data, "filter_name": filter_name, "table_name": table_name,
                             "facility": self.facility}
            oriya_payload1 = json.dumps(oriya_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                oriya_response_post = requests.request("POST",
                                                       sawaal_post_url,
                                                       data=oriya_payload1,
                                                       headers=headers,
                                                       auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as ex:
            messagebox.showinfo("PKAPP", ex)

        try:
            kannada_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_KANNADA.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            kannada_response_data = requests.request("GET", kannada_url, headers=headers)
            kannada_result_data = json.loads(kannada_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Kannada"

            kannada_payload = {"data": kannada_result_data, "filter_name": filter_name, "table_name": table_name,
                               "facility": self.facility}
            kannada_payload1 = json.dumps(kannada_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                kannada_response_post = requests.request("POST",
                                                         sawaal_post_url,
                                                         data=kannada_payload1,
                                                         headers=headers,
                                                         auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as kn:
            messagebox.showinfo("PKAPP", kn)

        try:
            gujarati_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_GUJARATI.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            gujarati_response_data = requests.request("GET", gujarati_url, headers=headers)
            gujarati_result_data = json.loads(gujarati_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "gujarati"

            gujarati_payload = {"data": gujarati_result_data, "filter_name": filter_name, "table_name": table_name,
                                "facility": self.facility}
            gujarati_payload1 = json.dumps(gujarati_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                gujarati_response_post = requests.request("POST",
                                                          sawaal_post_url,
                                                          data=gujarati_payload1,
                                                          headers=headers,
                                                          auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as gj:
            messagebox.showinfo("PKAPP", gj)

        try:
            english_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_ENGLISH.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            english_response_data = requests.request("GET", english_url, headers=headers)
            english_result_data = json.loads(english_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "English"

            english_payload = {"data": english_result_data, "filter_name": filter_name, "table_name": table_name,
                               "facility": self.facility}
            english_payload1 = json.dumps(english_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                english_response_post = requests.request("POST",
                                                         sawaal_post_url,
                                                         data=english_payload1,
                                                         headers=headers,
                                                         auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as en:
            messagebox.showinfo("PKAPP", en)

        try:
            telugu_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_TELUGU.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            telugu_response_data = requests.request("GET", telugu_url, headers=headers)
            telugu_result_data = json.loads(telugu_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Telugu"

            telugu_payload = {"data": telugu_result_data, "filter_name": filter_name, "table_name": table_name,
                              "facility": self.facility}
            telugu_payload1 = json.dumps(telugu_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                telugu_response_post = requests.request("POST",
                                                        sawaal_post_url,
                                                        data=telugu_payload1,
                                                        headers=headers,
                                                        auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as tlg:
            messagebox.showinfo("PKAPP", tlg)

        try:
            tamil_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_TAMIL.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            tamil_response_data = requests.request("GET", tamil_url, headers=headers)
            tamil_result_data = json.loads(tamil_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Tamil"

            tamil_payload = {"data": tamil_result_data, "filter_name": filter_name, "table_name": table_name,
                             "facility": self.facility}
            tamil_payload1 = json.dumps(tamil_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                tamil_response_post = requests.request("POST",
                                                       sawaal_post_url,
                                                       data=tamil_payload1,
                                                       headers=headers,
                                                       auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as tm:
            messagebox.showinfo("PKAPP", tm)

        try:
            punjabi_url = "http://rpi.prathamskills.org/aajkasawaal/AajKaSawal_PUNJABI.json"
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            sawaal_post_url = "http://localhost:8080/pratham/datastore/"

            punjabi_response_data = requests.request("GET", punjabi_url, headers=headers)
            punjabi_result_data = json.loads(punjabi_response_data.content.decode('utf-8'))

            self.facility = c.session()

            table_name = "AajKaSawaal"
            filter_name = "Punjabi"

            punjabi_payload = {"data": punjabi_result_data, "filter_name": filter_name, "table_name": table_name,
                               "facility": self.facility}
            punjabi_payload1 = json.dumps(punjabi_payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                punjabi_response_post = requests.request("POST",
                                                         sawaal_post_url,
                                                         data=punjabi_payload1,
                                                         headers=headers,
                                                         auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as pb:
            messagebox.showinfo("PKAPP", pb)

        try:
            headers = {
                'cache-control': "no-cache",
                'content-type': "application/json",
                'Accept': 'application/json'
            }

            self.facility = c.session()
            data_to_post = {
                "programId": str(self.programlist[self.program.get()]),
                "programName": self.program.get(),
                "State": self.states.get(),
                "StateCode": self.stateList[self.states.get()]
            }
            table_name = "ProgramState"
            filter_name = "programId:" + str(self.programlist[self.program.get()]) + ",state:" + \
                          self.stateList[self.states.get()]

            payload = {"data": data_to_post, "filter_name": filter_name, "table_name": table_name,
                       "facility": self.facility}
            payload1 = json.dumps(payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=headers, auth=("pratham", "pratham"))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                response_data_to_post = requests.request("POST",
                                                         "http://localhost:8080/pratham/datastore/",
                                                         data=payload1,
                                                         headers=headers,
                                                         auth=("pratham", "pratham"))
            except Exception as e:
                print(e)

            else:
                pass

        except Exception as e:
            messagebox.showinfo("PKAPP", e)

        messagebox.showinfo("PKAPP", "download process over")


app = CrlUI()
windowWidth = app.winfo_reqwidth()
windowHeight = app.winfo_reqheight()

positionRight = int(app.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(app.winfo_screenheight() / 6 - windowHeight / 2)

app.geometry("+{}+{}".format(positionRight, positionDown))
app.geometry("360x343")
app.mainloop()
