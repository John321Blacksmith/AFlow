"""
This module contains the functionality to format the scraped data to the Excel tables.
"""
import openpyxl
import pandas as pd

class Dumper:
	"""
	This class creates a data dumper object bound with 
	taken data as its attributes and performs operation
	based on the user's input.
	"""
	
	def __init__(
				self,
				filename,
				keyword,
				f_ext,
				list_of_objs,
				confs
			):
		self.filename = filename
		self.keyword = keyword
		self.f_ext = f_ext
		self.objs = list_of_objs
		self.confs = confs
		self.dataframe = pd.DataFrame(
								data=self.objs,
								columns=self.confs[self.keyword]['fields']
								)
		
	def write_to_excel(self):
		df = pd.DataFrame()
		df.to_excel()

	def write_to_json(self):
		df = pd.DataFrame()
		df.to_json()

	def write_to_csv(self):
		df = pd.DataFrame()
		df.to_csv()

	def write_to_text(self):
		pass


	def operate(self):
		"""
		Perform dumping the scraped data to the specified format.
		"""
		pass

