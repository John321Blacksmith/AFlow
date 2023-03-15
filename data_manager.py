"""
This module contains the functionality to format the scraped data to the Excel tables.
"""
import openpyxl
import pandas as pd


def write_objs_to_excel(file_name, sheet, list_of_objs: list, columns: list):
	"""
	This function takes a list of structured objects
	and records them to the dedicated excel table.
	"""

	# define a dataframe
	df = pd.DataFrame(data=list_of_objs, columns=columns)

	# perform writing to the excel file
	df.to_excel(file_name, sheet_name=sheet, index=False, engine='openpyxl')

	print('done')
