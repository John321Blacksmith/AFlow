"""
This module contains the functionality to format the scraped data to .csv format
and dump it to the Excel tables.
"""
from openpyxl import Workbook

# define a workbook
wb = Workbook()

# define a sheet
sheet = wb.active

# write the content to the columns A and B
sheet['A1'] = 'hello'
sheet['B1'] = 'world'


if __name__ == '__main__':
	wb.save(filename='hello_world.xlsx')