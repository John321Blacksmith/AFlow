"""
This module contains the functionality to format the scraped data to the Excel tables.
"""
import openpyxl
import pandas as pd


def write_objs_to_excel(file_name, list_of_objs: list):
	"""
	This function takes a list of structured objects
	and records them to the dedicated excel table.
	"""

	# define a dataframe
	df = pd.DataFrame(data=list_of_objs, columns=['title', 'integer', 'link', 'image'])

	# perform writing to the excel file
	df.to_excel(file_name, sheet_name='all_books', index=False, engine='openpyxl')

	print('done')
