books = {
	'books-to-scrape': {
		'source': 'http://books.toscrape.com/catalogue/page-{}.html',
		'object': {'tag': 'li', 'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'},
		'title': {'tag': 'h3'},
		'integer': {'tag': 'p', 'class': 'price_color'},
		'link': {'tag': 'a', 'attribute': 'src'},
		'image': {'tag': 'img', 'attribute': 'src'},
		'generic_quantity': {'tag': 'form', 'class': 'form-horizontal', 'inlined_tag': 'strong'},
		'obj_components': ['titles', 'integers', 'links', 'images']
	},

	'russian-books': {
		'source': 'https://www.books.ru/spravochniki-9001366/?page={}',
		'object':  {'tag': 'div', 'class': 'book-catalog_item'},
		'title': {'tag': 'a', 'class': 'custom-link book-catalog_item_title'},
		'integer': {'tag': 'span', 'class': 'book-price'},
		'link': {'tag': 'a'},
		'image': {'tag': 'img', 'attribute': 'src'},
		'generic_quantity': {'tag': 'span', 'class': 'catalog-category_value'},
		'obj_components': ['titles', 'integers', 'links', 'images']
	},

	'litres-books': {
		'source': 'https://www.litres.ru/genre/knigi-fantastika-5004/?page={}',
		'object': {'tag': 'div', 'class': 'Art-module__wrapper_8_qbP Minigrid__Art_nquiC'},
        'title': {'tag': 'div', 'class': 'Art-module__name__row_2S_Yp'},
        'integer': {'tag': 'p', 'class': 'RatingStars-module__value_2DvQU'},
        'link': {'tag': 'a', 'class': 'Art-module__imageWrapper_3sDLf'},
        'image': {'tag': 'img', 'class': 'newCover__cover_WLFHk', 'attribute': 'src'},
        'generic_quantity': '99071',
        'obj_components': ['titles', 'integers', 'links', 'images']
	}
}
