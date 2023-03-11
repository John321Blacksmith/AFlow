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
		'source': 'https://www.books.ru/bukhgalteriya-9000033/?page={}',
		'object':  {'tag': 'div', 'class': 'book-catalog_item'},
		'title': {'tag': 'a', 'class': 'custom-link book-catalog_item_title'},
		'integer': {'tag': 'span', 'class': 'book-price'},
		'link': {'tag': 'a'},
		'image': {'tag': 'img', 'attribute': 'src'},
		'generic_quantity': {'tag': 'span', 'class': 'catalog-category_value'},
		'obj_components': ['titles', 'integers', 'links', 'images']
	}
}
