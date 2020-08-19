import numpy as np
import pyautogui
import cv2

import pytesseract


class TableData:
    def __init__(self):
        self.balance1 = -1
        self.balance2 = -1
        self.balance3 = -1


class Parser:
    cf = 2.005
    table_width = int(1380 / cf)
    table_height = int(950 / cf)


    def __init__(self):
        self.tableData = TableData()

    def get_data(self):
        search_method = cv2.TM_SQDIFF_NORMED
        #checker_image = cv2.imread('checker_PS.png')
        checker_image = cv2.imread('star_PS.png')
        full_screen = pyautogui.screenshot()
        full_screen = cv2.cvtColor(np.array(full_screen), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(checker_image, full_screen, search_method)
        _, _, mnLoc, _ = cv2.minMaxLoc(result)
        table_x, table_y = mnLoc
        print("table x,y", table_x, table_y)

        real_table = full_screen[table_y:table_y + self.table_height, table_x:table_x + self.table_width]
        ### FOR TEST
        cv2.imwrite('real_table.png', real_table)
        ###

        self.get_parts(real_table)

    def get_parts(self, real_table):
        self.tableData.balance1 = self.get_part(real_table, int(695 / self.cf), int(725 / self.cf), int(645 / self.cf), int(790 / self.cf))

    def get_part(self, real_table, x0, x1, y0, y1):
        pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
        value = real_table[x0:x1, y0:y1]
        ### FOR TEST
        cv2.imwrite('tmp.png', value)
        cv2.dilate(value,(1000, 1000), value)
        ###
        text = pytesseract.image_to_string(value)
        text = text.strip()
        if text != "":
            print(text)
            if text.isdigit():
                return int(text)
            print("WARNING")
            return -1
        print("ERROR")
        return -1


p = Parser()
p.get_data()
