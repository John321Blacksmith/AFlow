"""
This module contains the data saving functionality.
"""
from configparser import ConfigParser


class DataBase:
	"""
	This object represents a database
	instance set with all the needed
	parameters.

	def get_params:
		:filename: str
		:section: str
		:return: dict

	def get_connection:
		:params: dict
		:return: psycopg2.Connection
	"""
	def __init__(self, filename):
		self.filename = filename

	def get_params(self) -> dict:
		"""
		Read the configuration file and
		form an object with parameters.
		"""

		# file parser
		parser = ConfigParser()

		# use the parser for file reading
		parser.read(self.file_name)

		# define a section for params allocation
		db = {}

		if parser.has_section(section):
			params = parser.items(section):
			for param in params:
				db[param[0]] = param[1]
		else:
			raise Exception(f'Section {section} not found in the file \'{self.filename}\'.')

		return db

	def get_connection(self):
		"""
		Take a parameters object and
		connect to the database.
		"""
		# read out new db params for connection
		params = self.get_params()
		# create a connection object
		connection = psycopg2.connect(params)

		return connection


class DataDumper:
	"""
	This object receives a list of python
	objects and puts each one as a DB record.
	
	def save_data:
		:list_of_objects: list[dict]
		:query_payload: dict
		:return: None
	"""
	def __init__(self, filename):
		self.database = DataBase(filename)

	def save_data(list_of_objects: list[dict], query_payload: dict):
		"""
		Take a list of pythonic objects and
		apply a query to the database to save
		them.
		"""

		with self.datadase.get_connection() as conn:
			cursor = conn.cursor()

			for i in range(0, len(list_of_objects)):
				cursor.execute(f"""INSERT INTO {query_payload['table']}(product, price, link, image)
									  VALUES(
									  		{list_of_objects[i]['product']},
									  		{list_of_objects[i]['price']},
									  		{list_of_objects[i]['link']},
									  		{list_of_objects[i]['image']}
									);""")
				conn.commit()
			conn.close()


class DataRetriever:
	"""
	This object takes a database instance
	and applies a query request for data
	extraction.

	def query_data:
		:db: DataBase
		:query_payload: dict
		:return: list[dict]
	"""
	...


class DataRemover:
	"""
	This object takes a database instance
	and removes the defined data from the DB.

	def remove_data:
		:db: DataBase
		:query_payload: dict
		:return: None
	"""
	...