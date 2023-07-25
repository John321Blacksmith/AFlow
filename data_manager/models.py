from pydantic import BaseModel


class Product(BaseModel):
	title: str
	image: str
	link: str
	price: float

