"""
Name:        main
Author:     范伟
Created:    2020/5/9下午6:32
IDE:        PyCharm
"""
import json
import re
from urllib.parse import urlencode

import requests
from pyquery import PyQuery

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib


class FName:
    base_url = "https://www.mzi8.com"

    def __init__(self):
        self.boys_name_list = []
        self.girls_name_list = []
        self.boys_name_info_list = []
        self.girls_name_info_list = []

    def save_name_file(self):
        self.get_names()
        self.name_info_handle()

    def get_names(self):
        for page in range(1, 51):
            options = dict(
                sign="fy", xing="范", mzi="", wz="", ymd="2020-06-10", lx=1, gs=0, yy="", ff=1, page=page
            )
            url = "{}/qiming/s2.php?{}".format(self.base_url, urlencode(options))
            print("名字列表:", url)
            res = requests.get(url)
            if res.status_code == 200:
                res.encoding = "UTF-8"
                doc = PyQuery(res.text)
                name_li_items = doc("#show_liebiao #mz-liebiao-ym .am-hide").items()
                name_index = 1
                for name_li in name_li_items:
                    name_list = name_li.text().split(" ")
                    new_name_list = self.name_list_handle(name_list)
                    if name_index % 2 == 0:
                        self.girls_name_list += new_name_list
                    else:
                        self.boys_name_list += new_name_list
                    name_index += 1

    @staticmethod
    def name_list_handle(name_list):
        new_name_list = []
        for name in name_list:
            if "范" != name:
                new_name_list.append("范{}".format(name))
        return new_name_list

    def name_info_handle(self):
        for name in self.boys_name_list:
            name_info = self.get_name_info(name, 1)
            if name_info:
                self.boys_name_info_list.append(name_info)
                with open("boys_name_info.json", "w") as fp:
                    fp.write(json.dumps(self.boys_name_info_list, indent=4, ensure_ascii=False))

        for name in self.girls_name_list:
            name_info = self.get_name_info(name, 0)
            if name_info:
                self.girls_name_info_list.append(name_info)
                with open("girls_name_info.json", "w") as fp:
                    fp.write(json.dumps(self.girls_name_info_list, indent=4, ensure_ascii=False))

    def get_name_info(self, name, xb):
        name_info = dict()
        options = dict(
            ac="lb", sign="cha", xing=name[:1], xb=xb, ymd="2020-06-10", h="", i="", ming=name[1:]
        )
        url = "{}/ceshi/c.php?{}".format(self.base_url, urlencode(options))
        print("名字详情", name, url)
        res = requests.get(url)
        if res.status_code == 200:
            res.encoding = "UTF-8"
            if "错误" not in res.text:
                doc = PyQuery(res.text)
                name_info['name'] = name
                name_info['pinyin'] = doc(".title .py").text().replace("(", "").replace(")", "")
                name_info['score'] = int(doc(".title .dafen").text())
                name_info['impression'] = doc(".mod2 .con20 .yy").text()
                name_info['popularity'] = doc(".con40").text()
                name_info['coincidence_rate'] = float(
                    re.sub(
                        "[^0-9.\-]", "", doc(".li-s").filter(
                            lambda i: "姓名“{}”重合率".format(name) in PyQuery(this).text()
                        ).text()
                    )
                )
                name_info['pwt_name'] = self.get_pet_name(name)

        return name_info

    def get_pet_name(self, name):
        pet_name_list = []
        url = "{}/qxm/xm_{}.html".format(self.base_url, name)
        res = requests.get(url)
        if res.status_code == 200:
            res.encoding = "UTF-8"
            doc = PyQuery(res.text)
            pet_name_items = doc(".mz-xm-l").items()
            moral_item = doc(".mz-xiaoming-li .mz-xm-s").filter(lambda i: "寓意" in PyQuery(this).text())
            index = 1
            for pet_name_item in pet_name_items:
                popularity = pet_name_item("img").attr("src")
                popularity = int(re.sub("\D", "", popularity))
                if popularity >= 4:
                    pet_name_info = dict()
                    pet_name_info['pet_name'] = pet_name_item("a").text()
                    pet_name_info['popularity'] = popularity
                    pet_name_info['moral'] = moral_item.eq(index).text()
                    pet_name_list.append(pet_name_info)
                index += 1

        return pet_name_list


if __name__ == "__main__":
    # FName().get_name_info("范言正", 1)
    FName().save_name_file()
