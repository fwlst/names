import json
import time

import requests
import xlrd
from pyquery import PyQuery


class Idiom:

    def __init__(self):
        self.idiom_info_list = []
        self.category_list = []
        self.get_category()

    def get_all_idiom_info(self):
        for category_info in self.category_list:
            print(category_info)
            self.aaa(**category_info)

    def aaa(self, url, category, keyword):
        try:
            self.get_antonym(url, category, keyword)
        except:
            self.aaa(url, category, keyword)

    def get_category(self):
        res = requests.get("http://cy.5156edu.com/")
        if res.status_code == 200:
            res.encoding = "gb2312"
            doc = PyQuery(res.text)
            common_table_obj = doc("#table1 table tr").eq(11)
            common_table_list = common_table_obj("table td").items()
            for common_table in common_table_list:
                category = common_table.text()
                if "成语" in category:
                    category = category.replace("成语", "")
                    url = "http://cy.5156edu.com{}".format(common_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category=category, keyword=None)
                    )

            season_table_obj = doc("#table1 table tr").eq(15)
            season_table_list = season_table_obj("table td").items()
            for season_table in season_table_list:
                category = season_table.text()
                if "成语" in category:
                    category = category.replace("成语", "")
                    category = category.replace("的", "")
                    url = "http://cy.5156edu.com/{}".format(season_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category="季节气候", keyword=category)
                    )

            chinese_zodiac_table_obj = doc("#table1 table tr").eq(22)
            chinese_zodiac_table_list = chinese_zodiac_table_obj("table td").items()
            for chinese_zodiac_table in chinese_zodiac_table_list:
                category = chinese_zodiac_table.text()
                if "成语" in category:
                    category = category.replace("成语", "")
                    category = category.replace("的", "")
                    url = "http://cy.5156edu.com/{}".format(chinese_zodiac_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category="十二生肖", keyword=category)
                    )

            chinese_zodiac_table_obj = doc("#table1 table tr").eq(27)
            chinese_zodiac_table_list = chinese_zodiac_table_obj("table td").items()
            for chinese_zodiac_table in chinese_zodiac_table_list:
                category = chinese_zodiac_table.text()
                if "成语" in category:
                    category = category.replace("成语", "")
                    category = category.replace("的", "")
                    url = "http://cy.5156edu.com/{}".format(chinese_zodiac_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category="动物", keyword=category)
                    )

            chinese_zodiac_table_obj = doc("#table1 table tr").eq(32)
            chinese_zodiac_table_list = chinese_zodiac_table_obj("table td").items()
            for chinese_zodiac_table in chinese_zodiac_table_list:
                category = chinese_zodiac_table.text()
                if "成语" in category:
                    category = category.replace("成语", "")
                    category = category.replace("的", "")
                    url = "http://cy.5156edu.com/{}".format(chinese_zodiac_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category="数字", keyword=category)
                    )

            chinese_zodiac_table_obj = doc("#table1 table tr").eq(37)
            chinese_zodiac_table_list = chinese_zodiac_table_obj("table td").items()
            for chinese_zodiac_table in chinese_zodiac_table_list:
                category = chinese_zodiac_table.text()
                if "成语" in category:
                    category = category.replace("成语", "")
                    category = category.replace("的", "")
                    url = "http://cy.5156edu.com/{}".format(chinese_zodiac_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category="描写心情", keyword=category)
                    )

            chinese_zodiac_table_obj = doc("#table1 table tr").eq(42)
            chinese_zodiac_table_list = chinese_zodiac_table_obj("table td").items()
            for chinese_zodiac_table in chinese_zodiac_table_list:
                category = chinese_zodiac_table.text()
                if "成语" in category or "四字" in category:
                    url = "http://cy.5156edu.com/{}".format(chinese_zodiac_table("a").attr("href"))
                    self.category_list.append(
                        dict(url=url, category=None, keyword=None)
                    )

    def get_antonym(self, url, category, keyword):
        res = requests.get(url)
        if res.status_code == 200:
            res.encoding = "gb2312"
            doc = PyQuery(res.text)
            table_num = len([i for i in doc("table table").items()])
            print(table_num)
            if table_num == 9:
                antonym_table_obj = doc("table table").eq(7)
                antonym_obj_list = antonym_table_obj("td").items()
                self.save_idiom_info(antonym_obj_list, category, keyword)
            elif table_num == 11:
                antonym_table_obj = doc("table table").eq(6)
                antonym_obj_list = antonym_table_obj("td a").items()
                self.save_idiom_info(antonym_obj_list, category, keyword)
            else:
                print("成语列表解析失败")

    def save_idiom_info(self, obj_list, category, keyword):
        for table in obj_list:
            info_url = "http://cy.5156edu.com{}".format(table("a").attr("href"))
            print(info_url)
            idiom_info = self.get_idiom_info(info_url, category, keyword)
            if idiom_info.get("idiom"):
                self.idiom_info_list.append(idiom_info)
                print(len(self.idiom_info_list), idiom_info)
                with open("idiom_info_list.json", "w") as fp:
                    fp.write(json.dumps(self.idiom_info_list, indent=4, ensure_ascii=False))
            else:
                print("获取失败", idiom_info)
            time.sleep(1)

    @staticmethod
    def get_idiom_info(info_url, category, keyword):
        print("详情URL", info_url)
        res = requests.get(info_url)
        if res.status_code == 200:
            res.encoding = "gb2312"
            doc = PyQuery(res.text)
            antonym_table_obj = doc("#table3 table").eq(0)
            if antonym_table_obj(".font_22"):
                pinyin = antonym_table_obj(".font_18").text()
                homoionym = antonym_table_obj("tr").eq(1)("td").eq(1).text()
                antonym = antonym_table_obj("tr").eq(1)("td").eq(3).text()
                usage = antonym_table_obj("tr").eq(2)("td").eq(1).text()
                explain = antonym_table_obj("tr").eq(3)("td").eq(1).text()
                source = antonym_table_obj("tr").eq(4)("td").eq(1).text()
                example = antonym_table_obj("tr").eq(5)("td").eq(1).text()
                allegorical_sayings = antonym_table_obj("tr").eq(6)("td").eq(1).text()
                riddle = antonym_table_obj("tr").eq(7)("td").eq(1).text()
                idiom_story = antonym_table_obj("tr").eq(8)("td").eq(1).text()
                idiom_info = dict(
                    idiom=antonym_table_obj(".font_22").text(),
                    pinyin=pinyin if pinyin else None,
                    homoionym=homoionym if homoionym else None,
                    antonym=antonym if antonym else None,
                    usage=usage if usage else None,
                    explain=explain if explain else None,
                    source=source if source else None,
                    example=example if example else None,
                    allegorical_sayings=allegorical_sayings if allegorical_sayings else None,
                    riddle=riddle if riddle else None,
                    idiom_story=idiom_story if idiom_story else None,
                    category=category,
                    keyword=keyword
                )
            else:
                print(antonym_table_obj("tr").eq(0).text())
                pinyin = antonym_table_obj("tr").eq(1)("td").eq(1).text()
                homoionym = antonym_table_obj("tr").eq(2)("td").eq(1).text()
                antonym = antonym_table_obj("tr").eq(2)("td").eq(3).text()
                usage = antonym_table_obj("tr").eq(3)("td").eq(1).text()
                explain = antonym_table_obj("tr").eq(4)("td").eq(1).text()
                source = antonym_table_obj("tr").eq(5)("td").eq(1).text()
                example = antonym_table_obj("tr").eq(6)("td").eq(1).text()
                allegorical_sayings = antonym_table_obj("tr").eq(7)("td").eq(1).text()
                riddle = antonym_table_obj("tr").eq(8)("td").eq(1).text()
                idiom_story = antonym_table_obj("tr").eq(9)("td").eq(1).text()
                idiom_info = dict(
                    idiom=antonym_table_obj("tr").eq(0).text(),
                    pinyin=pinyin if pinyin else None,
                    homoionym=homoionym if homoionym else None,
                    antonym=antonym if antonym else None,
                    usage=usage if usage else None,
                    explain=explain if explain else None,
                    source=source if source else None,
                    example=example if example else None,
                    allegorical_sayings=allegorical_sayings if allegorical_sayings else None,
                    riddle=riddle if riddle else None,
                    idiom_story=idiom_story if idiom_story else None,
                    category=category,
                    keyword=keyword
                )
                print(idiom_info)
        else:
            idiom_info = dict()
        return idiom_info


if __name__ == "__main__":
    Idiom().get_all_idiom_info()
