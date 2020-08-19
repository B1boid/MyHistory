import numpy as np
import pyautogui
import cv2
import re

from pytesseract import image_to_string, pytesseract


class Player:
    def __init__(self):
        self.balance = -1
        self.bet = -1
        self.cards = (-1, -1)


class TableData:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()


class Parser:
    cf = 2.005
    table_width = int(1380 / cf)
    table_height = int(950 / cf)

    def __init__(self):
        self.tableData = TableData()
        pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

    def get_data(self):
        search_method = cv2.TM_SQDIFF_NORMED
        checker_image = cv2.imread('star_PS.png')
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
        self.tableData.player1.balance = self.get_part(real_table,
                                                       int(695 / self.cf),
                                                       int(725 / self.cf),
                                                       int(545 / self.cf),
                                                       int(790 / self.cf))
        self.tableData.player2.balance = self.get_part(real_table,
                                                       int(215 / self.cf),
                                                       int(265 / self.cf),
                                                       int(100 / self.cf),
                                                       int(250 / self.cf))
        self.tableData.player3.balance = self.get_part(real_table,
                                                       int(215 / self.cf),
                                                       int(265 / self.cf),
                                                       int(1125 / self.cf),
                                                       int(1275 / self.cf))

        firstCardHand = self.get_part(real_table,
                                      int(570 / self.cf),  # y0
                                      int(655 / self.cf),  # y1
                                      int(575 / self.cf),  # x0
                                      int(690 / self.cf))  # x1

        secondCardHand = self.get_part(real_table,
                                       int(570 / self.cf),
                                       int(655 / self.cf),
                                       int(575 / self.cf),
                                       int(780 / self.cf))

        flop1 = self.get_part(real_table,
                              int(300 / self.cf),
                              int(400 / self.cf),
                              int(445 / self.cf),
                              int(545 / self.cf))
        flop2 = self.get_part(real_table,
                              int(300 / self.cf),
                              int(400 / self.cf),
                              int(545 / self.cf),
                              int(645 / self.cf))
        flop3 = self.get_part(real_table,
                              int(300 / self.cf),
                              int(400 / self.cf),
                              int(645 / self.cf),
                              int(730 / self.cf))

        tern = self.get_part(real_table,
                             int(300 / self.cf),
                             int(400 / self.cf),
                             int(730 / self.cf),
                             int(830 / self.cf))
        river = self.get_part(real_table,
                              int(300 / self.cf),
                              int(400 / self.cf),
                              int(830 / self.cf),
                              int(930 / self.cf))

    def get_part(self, real_table, x0, x1, y0, y1):
        value = real_table[x0:x1, y0:y1]
        ### FOR TEST
        cv2.imwrite('tmp.png', value)
        ###
        text = image_to_string(value)
        text = text.strip().replace(".", "").replace(",", "")
        text = re.sub("\D[^a-zA-Z][^-]", "", text)
        if text != "":
            print(text)
            if text.isdigit():
                return int(text)
            if text.find("All-in") > -1 or text.find("AlHn"):
                return -3
            if text.find("Sitting Out") > -1:
                return -2
            print("WARNING")
            return -1
        print("ERROR")
        return -1


p = Parser()
p.get_data()
