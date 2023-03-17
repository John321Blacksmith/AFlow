"""
This module contains the functionality to format the scraped data to the Excel tables.
"""
import json
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
		self.keyword = keyword
		self.f_ext = f_ext
		self.objs = list_of_objs
		self.confs = confs
		# define a dataframe
		self.dataframe = pd.DataFrame(
								data=self.objs,
								columns=self.confs[self.keyword]['fields']
								)

	# define which directory the file goes to
	_storage = self.confs[self.keyword]['storage_name'] + '/' + filename

	def write_to_excel(self):
		self.dataframe.to_excel(self._storage, index=False, engine='openpyxl')


	def write_to_json(self):
		self.dataframe.to_json(self._storage)


	def write_to_csv(self):
		self.dataframe.to_csv(self._storage, index=False)


	def write_to_text(self):
		with open(self._storage, mode='w', encoding='utf-8') as f:
			row = 0
			headers = self.confs[self.keyword]['fields']
			for i in range(0, len(self.objs)):
				for key, value in self.objs[i].items():
					if i == 0:
						f.writerow(headers)
						i += 1
					else:
						f.writerow((key, value))


	def operate(self):
		"""
		Perform dumping the scraped data to the specified format.
		"""
		# this control flow defines which method
		# to use accordingly the specified extention 
		if self.f_ext == 'excel':
			self.write_to_excel()
		elif self.f_ext == 'cvs':
			self.write_to_csv()
		elif self.f_ext == 'json':
			self.write_to_json()
		else:
			self.write_to_text()

