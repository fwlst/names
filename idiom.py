import xlrd


class Idiom:

    def __init__(self):
        self.idiom_info_list = []
        self.read_file_xlsx()
        pass

    def read_file_xlsx(self):
        data = xlrd.open_workbook('idiom.xlsx')
        table = data.sheet_by_name('叠词格式成语')
        # 获取总行数
        rows = table.nrows
        # 获取总列数
        cols = table.ncols
        idiom_list = []

        for x in range(1, rows):
            idiom_info = dict(
                idiom=None,
                classify=[],
                notes=None,
            )
            for y in range(1, cols):
                if y == 1:
                    idiom_info["idiom"] = table.cell(x, y).value if table.cell(x, y).value else None
                elif y == 2:
                    idiom_info["notes"] = table.cell(x, y).value if table.cell(x, y).value else None
                elif y == 3:
                    classify = table.cell(x, y).value
                    if "字成语" in classify and "数字成语" not in classify:
                        idiom_info["classify"] = None
                    elif "关于" in classify:
                        idiom_info["classify"] = None
                    else:
                        idiom_info["classify"] = table.cell(x, y).value if table.cell(x, y).value else None

            idiom = idiom_info.get("idiom")
            if idiom:
                if idiom not in idiom_list:
                    idiom_list.append(idiom)
                    self.idiom_info_list.append(idiom_info)
                else:
                    print(idiom not in idiom_list, idiom_info)


if __name__ == "__main__":
    Idiom()
