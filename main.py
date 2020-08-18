import numpy as np
import pyautogui
import cv2

from pytesseract import image_to_string



class TableData:
    def __init__(self):
        self.balance1 = -1
        self.balance2 = -1
        self.balance3 = -1


class Parser:
    table_width = 1380
    table_height = 950

    def __init__(self):
        self.tableData = TableData()

    def get_data(self):
        search_method = cv2.TM_SQDIFF_NORMED
        checker_image = cv2.imread('checker_PS.png')
        full_screen = pyautogui.screenshot()
        full_screen = cv2.cvtColor(np.array(full_screen), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(checker_image, full_screen, search_method)
        _, _, mnLoc, _ = cv2.minMaxLoc(result)
        table_x, table_y = mnLoc
        print("table x,y =", table_x, table_y)

        real_table = full_screen[table_y:table_y + self.table_height, table_x:table_x + self.table_width]
        real_table = ~real_table

        ### FOR TEST
        cv2.imwrite('real_table.png', real_table)
        ###

        self.get_parts(real_table)

    def get_parts(self, real_table):
        self.tableData.balance1 = self.get_part(real_table, 695, 725, 650, 790)

    def get_part(self, real_table, x0, x1, y0, y1):
        value = real_table[x0:x1, y0:y1]
        ### FOR TEST
        cv2.imwrite('tmp.png', value)
        ###
        text = image_to_string(value)
        text = text.strip().replace(".","").replace(",","")
        if text != "":
            print(text)
            if text.isdigit():
                return int(text)
            if text.join("All-in"):
                return -3
            if text.join("Sitting Out"):
                return -2
            print("WARNING")
            return -1
        print("ERROR")
        return -1


p = Parser()
p.get_data()
