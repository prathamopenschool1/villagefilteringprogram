#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pprint import pprint

from check import check_internet
import requests
import json
from tkinter import messagebox
from collections import OrderedDict
# import csv
# import pandas as pd


class LiveCall(object):
    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        'Accept': 'application/json'
    }

    program_dict = OrderedDict()
    state_dict = OrderedDict()

    programid = ''
    state = ''
    block_name = ''
    district = ''

    crl_url = "http://www.hlearning.openiscool.org/api/crl/get/"
    village_url = "http://www.hlearning.openiscool.org/api/village/get/"

    program_url = "http://swap.prathamcms.org/api/program"
    state_url = "http://swap.prathamcms.org/api/state?progid="

    # post api
    url_post = "http://localhost:8080/pratham/datastore/"

    # session api
    session_url = "http://localhost:8080/api/session/"

    # authentication
    username = "pratham"
    password = "pratham"

    querystring = {"programid": programid, "state": state}

    session_payload = "grant_type=password&username=pratham&password=pratham"
    session_headers = {
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }

    village_data = ''

    blockslist = set()
    myblocklist = ''

    villageslist = set()
    myvillagelist = ''

    district_list = set()
    district_lists = ''

    def getprogramlist(self):
        # check_internet()
        # programs list call
        programs_api_response = requests.request("GET", self.program_url, headers=self.headers)
        programs_api_result = json.loads(programs_api_response.content.decode("utf-8"))

        for values in programs_api_result:
            self.program_dict[values['ProgramName']] = values['ProgramId']

        return self.program_dict

    def getstatelist(self, program_id):
        # check_internet()
        self.state_dict = {}
        # state list call
        states_api_response = requests.request("GET", self.state_url + str(program_id), headers=self.headers)
        states_api_result = json.loads(states_api_response.content.decode("utf-8"))

        for st in states_api_result:
            self.state_dict[st['StateName']] = st['StateCode']

        return self.state_dict

    def session(self):

        global facility_id

        response = requests.request("POST", self.session_url, data=self.session_payload, headers=self.session_headers)
        result = json.loads(response.content.decode('utf-8'))
        facility_id = result['facility_id']
        return facility_id

    def crl_call(self, p, s):
        self.session()

        self.programid = p
        self.state = s

        querystring = {"programid": self.programid, "state": self.state}

        response_crl = requests.request("GET", self.crl_url, headers=self.headers, params=querystring)
        res_crl = json.loads(response_crl.content.decode("utf-8"))
        # global users_list, passwords_list
        # users_list = []
        # passwords_list = []
        # for k in res_crl:
        #     users_list.append(k['UserName'])
        #     passwords_list.append(k['Password'])

        # rows = zip(users_list, passwords_list)
        # with open('/home/pi/superusers.csv', "w") as out:
        #     writer = csv.writer(out)
        #     for row in rows:
        #         writer.writerow(row)
        # pd.DataFrame(list(zip(users_list, passwords_list))).to_csv('/home/pi/output.csv',
        #                                                            header=False, index=False)
        table_name = "Crl"
        filter_name = "programid:" + self.programid + ",state:" + self.state

        payload = {"data": res_crl, "filter_name": filter_name, "table_name": table_name, "facility": facility_id}
        payload1 = json.dumps(payload)

        url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
            filter_name, table_name)

        response1 = requests.request("GET", url_del, headers=self.headers, auth=(self.username, self.password))
        res1 = json.loads(response1.content.decode("utf-8"))

        for pid in res1:
            if filter_name and table_name in url_del:
                show_id = pid['id']
                url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                try:
                    res_del = requests.delete(url_del1, headers=self.headers)
                except Exception as e:
                    messagebox.showinfo("PKAPP", "some problem occurred")
            else:
                pass
        try:
            response_crl_post = requests.request("POST", self.url_post, data=payload1, headers=self.headers,
                                                 auth=(self.username, self.password))
        except Exception as e:
            messagebox.showinfo("PKAPP", "Problem occurred while loading please check internet connection")

    def district_call(self, p, s):

        self.district_list = set()

        self.session()

        self.programid = p
        self.state = s

        querystring = {"programid": self.programid, "state": self.state}

        global res_village, response_village
        response_village = requests.request("GET", self.village_url, headers=self.headers, params=querystring)
        res_village = json.loads(response_village.content.decode("utf-8"))
        self.village_data = res_village

        for dist in self.village_data:
            dist = dist['District']
            self.district_list.add(dist)

        self.district_lists = list(self.district_list)
        self.district_lists = sorted(self.district_lists)

        return self.district_lists

    def block_call(self, p, s, d):
        self.blockslist = set()

        self.session()

        self.programid = p
        self.state = s
        self.district = d

        for block in res_village:
            if block['District'] == self.district:
                self.blockslist.add(block['Block'])

        self.myblocklist = list(self.blockslist)
        self.myblocklist = sorted(self.myblocklist)

        return self.myblocklist

    def villages_call(self, p, s, b):
        self.session()
        self.programid = p
        self.state = s
        self.block_name = b

        self.villageslist = set()
        for value in res_village:
            if value['Block'] == self.block_name:
                self.villageslist.add(value['VillageName'])

        self.myvillagelist = list(self.villageslist)
        self.myvillagelist = sorted(self.villageslist)

        return self.myvillagelist

    def allvillage_call(self):
        return res_village

    def postvillage(self, p, s, b, av, v):
        self.session()
        self.programid = p
        self.state = s
        self.block_name = b

        villages_to_post = []
        global res_village

        for vn1 in v:
            for vn in av:
                if vn1 == vn['VillageName']:
                    villages_to_post.append(vn)

        table_name = "village"
        filter_name = "programid:" + self.programid + ",state:" + self.state

        url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
            filter_name, table_name)

        response1 = requests.request("GET", url_del, headers=self.headers,
                                     auth=(self.username, self.password))
        res_village = json.loads(response1.content.decode("utf-8"))

        for vobj in villages_to_post:
            for resv in res_village:
                if vobj['VillageId'] == resv['data']['VillageId']:
                    show_id = resv['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=self.headers)
                        # print("deleted")
                    except:
                        print(res_del.status_code, res_del.reason)

            payload_village = {"data": vobj, "filter_name": filter_name, "table_name": table_name,
                               "facility": facility_id}
            payload_village1 = json.dumps(payload_village)

            try:
                response_village_post = requests.request("POST", self.url_post, data=payload_village1,
                                                         headers=self.headers,
                                                         auth=(self.username, self.password))
            except Exception as e:
                messagebox.showinfo("PKAPP", e)
                # print(e)

        for i in villages_to_post:
            i = i["VillageId"]
            group = "http://www.devtab.openiscool.org/api/Group/?programid=%s&villageId=%s" % (self.programid, i)
            querystring1 = {"programid": self.programid, "villageid": i}
            response_group = requests.request("GET", group, headers=self.headers, params=querystring1)
            res_group = json.loads(response_group.content.decode("utf-8"))
            table_name = "group"
            filter_name = "programid:" + self.programid + ",villageid:" + str(i)
            payload = {"data": res_group, "filter_name": filter_name, "table_name": table_name, "facility": facility_id}
            payload1 = json.dumps(payload)
            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (filter_name,
                                                                                                 table_name)
            response1 = requests.request("GET", url_del, headers=self.headers, auth=(self.username, self.password))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=self.headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                response_post_group = requests.request("POST", self.url_post, data=payload1, headers=self.headers,
                                                       auth=(self.username, self.password))
                # print(response_post_group.status_code, response_post_group.reason)
            except Exception as e:
                messagebox.showinfo("PKAPP", "Problem occurred while loading please check internet connection")

        for i in villages_to_post:
            i = i["VillageId"]
            student = "http://www.devtab.openiscool.org/api/student/?programid=%s&villageId=%s" % (self.programid, i)
            querystring1 = {"programid": self.programid, "villageid": i}
            response_std = requests.request("GET", student, headers=self.headers, params=querystring1)
            res_std = json.loads(response_std.content.decode("utf-8"))
            table_name = "student"
            filter_name = "programid:" + self.programid + ",villageid:" + str(i)

            payload = {"data": res_std, "filter_name": filter_name, "table_name": table_name, "facility": facility_id}
            payload1 = json.dumps(payload)

            url_del = "http://localhost:8080/pratham/datastore/?filter_name=%s&table_name=%s" % (
                filter_name, table_name)

            response1 = requests.request("GET", url_del, headers=self.headers, auth=(self.username, self.password))
            res1 = json.loads(response1.content.decode("utf-8"))

            for pid in res1:
                if filter_name and table_name in url_del:
                    show_id = pid['id']
                    url_del1 = "http://localhost:8080/pratham/datastore/" + show_id
                    try:
                        res_del = requests.delete(url_del1, headers=self.headers)
                    except Exception as e:
                        messagebox.showinfo("PKAPP", "some problem occurred")
                else:
                    pass

            try:
                response_post_std = requests.request("POST", self.url_post, data=payload1, headers=self.headers,
                                                     auth=(self.username, self.password))
            except Exception as e:
                messagebox.showinfo("PKAPP", "Problem occurred while loading please check internet connection")

        # for i in villages_to_post:
        #     i = i["VillageId"]
        #     learner = "http://www.devtab.openiscool.org/api/CoachYouth/?programid=%s&villageId=%s" % (self.programid, i)
        #     querystring1 = {"programid": self.programid, "villageid": i}
        #     response_learner = requests.request("GET", learner, headers=self.headers, params=querystring1)
        #     res_learner = json.loads(response_learner.content.decode("utf-8"))
        #     # pprint(res_learner)
        #     global users1_list, passwords1_list, full_Name
        #     users1_list = []
        #     passwords1_list = []
        #     full_Name = []
        #     for k in res_learner:
        #         users1_list.append(k['UserName'])
        #         passwords1_list.append(k['Password'])
        #         full_Name.append(k['CoachName'])
        #
        #     # rows = zip(full_Name, users1_list, passwords1_list)
        #     # with open('/home/pi/learners.csv', "w") as out:
        #     #     writer = csv.writer(out)
        #     #     for row in rows:
        #     #         writer.writerow(row)
        #
        #     pd.DataFrame(list(zip(full_Name, users1_list, passwords1_list))).to_csv('/home/pi/learners.csv',
        #                                                                             header=False, index=False)
