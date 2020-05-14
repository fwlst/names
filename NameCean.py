"""
Name:        NameCean
Author:     范伟
Created:    2020/5/13上午9:52
IDE:        PyCharm
"""
import json


class FName:

    def __init__(self):
        self.boys_name_info_list = []
        self.girls_name_info_list = []
        self.new_boys_name_info_list = []
        self.new_girls_name_info_list = []
        self.boys_name_list = []
        self.girls_name_list = []

    def boys_score_filter(self, n):
        if n.get("name") in self.boys_name_list:
            return False
        else:
            self.boys_name_list.append(n.get("name"))
            return n.get("score") >= 93

    def girls_score_filter(self, n):
        if n.get("name") in self.girls_name_list:
            return False
        else:
            self.girls_name_list.append(n.get("name"))
            return n.get("score") >= 93

    def filter_name_info(self):
        self.read_name_file()
        print(len(self.boys_name_info_list))
        self.new_boys_name_info_list = list(filter(self.boys_score_filter, self.boys_name_info_list))
        print(len(self.new_boys_name_info_list))

        print(len(self.girls_name_info_list))
        self.new_girls_name_info_list = list(filter(self.girls_score_filter, self.girls_name_info_list))
        print(len(self.new_girls_name_info_list))

        self.save_name_file()

    def read_name_file(self):
        with open("girls_name_info.json", "r") as fp:
            self.girls_name_info_list = json.load(fp)

        with open("boys_name_info.json", "r") as fp:
            self.boys_name_info_list = json.load(fp)

    def save_name_file(self):
        with open("new_girls_name_info_list.json", "w") as fp:
            fp.write(json.dumps(self.new_girls_name_info_list, indent=4, ensure_ascii=False))

        with open("new_boys_name_info_list.json", "w") as fp:
            fp.write(json.dumps(self.new_boys_name_info_list, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    FName().filter_name_info()
