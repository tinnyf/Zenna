from gspread_formatting import *

import gspread

from discord.ext import commands

class GoogleSheets:

    def __init__(self):
        self.gc = gspread.service_account(filename = "zatu-integration-b45b5d137434.json")
        self.sheet = self.gc.open("DISCORD CODES FOR WINNERS")
        self.worksheet = self.sheet.get_worksheet(0)

    def find_cell(self, value):
        return self.worksheet.find(value)

    def get_next_cell(self, cell):
        return self.worksheet.cell(cell.row, cell.col + 1)

    def get_values(self, column):
        return self.worksheet.col_values(column)

    def set_cell(self, cell, value):
        self.worksheet.update_cell(cell.row, cell.col, value)

    def first_blank(self, column): # -> gspread.cell
        row = 0
        for index, value in enumerate(self.worksheet.col_values(column + 1)):
            row = index
            if value is None:
                break
        return self.worksheet.cell(int(row + 2), int(column))

    def mark_used(self, cell):
        self.worksheet.format(cell.address, {
            "backgroundColor":{ "red" :106/255, "green": 168/255, "blue": 79/255}, "textFormat": {"foregroundColor": {"red": 255/255, "green":255/255 , "blue":255/255}}
        }),


    def get_remaining(self, column):
        total = 0
        second_total = 0
        for count, value in enumerate(self.worksheet.col_values(column)):
            if value == '':
                total = count - 1
                break
            total = count

        for count,value in enumerate(self.worksheet.col_values(column + 1)):
            if value == '':
                second_total = count -1
                break
            second_total = count
        return (total - second_total)



