books = {
	'storage_name': 'tables',
	'books-to-scrape': {
		'source': 'http://books.toscrape.com/catalogue/page-{}.html',
		'object': {'tag': 'li', 'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'},
		'title': {'tag': 'h3'},
		'integer': {'tag': 'p', 'class': 'price_color'},
		'link': {'tag': 'a', 'attribute': 'src'},
		'image': {'tag': 'img', 'attribute': 'src'},
		'generic_quantity': {'tag': 'form', 'class': 'form-horizontal', 'inlined_tag': 'strong'},
		'obj_components': ['titles', 'integers', 'links', 'images'],
		'fields': ['title', 'price', 'link', 'image']
	},

	'russian-books': {
		'source': 'https://www.books.ru/spravochniki-9001366/?page={}',
		'object':  {'tag': 'div', 'class': 'book-catalog_item'},
		'title': {'tag': 'a', 'class': 'custom-link book-catalog_item_title'},
		'integer': {'tag': 'span', 'class': 'book-price'},
		'link': {'tag': 'a'},
		'image': {'tag': 'img', 'attribute': 'src'},
		'generic_quantity': {'tag': 'span', 'class': 'catalog-category_value'},
		'obj_components': ['titles', 'integers', 'links', 'images'],
		'fields': ['title', 'price', 'link', 'image']
	},

	'litres-books': {
		'source': 'https://www.litres.ru/genre/knigi-fantastika-5004/',
		'object': {'tag': 'div', 'class': 'Art-module__wrapper_8_qbP Minigrid__Art_nquiC'},
        'title': {'tag': 'div', 'class': 'Art-module__name__row_2S_Yp'},
        'integer': {'tag': 'p', 'class': 'RatingStars-module__value_2DvQU'},
        'link': {'tag': 'a', 'class': 'Art-module__imageWrapper_3sDLf'},
        'image': {'tag': 'img', 'class': 'newCover__cover_WLFHk', 'attribute': 'src'},
        'generic_quantity': '99071',
        'obj_components': ['titles', 'integers', 'links', 'images'],
        'fields': ['title', 'price', 'link', 'image']
	},

	'ali-books': {
		'source': 'https://aliexpress.ru/category/205958512/books-new.html?g=y&page={}',
		'object': {'tag': 'div', 'class': 'product-snippet_ProductSnippet__content__52z59'},
		'title': {'tag': 'div', 'class': 'product-snippet_ProductSnippet__name__52z59'},
		'integer': {'tag': 'div', 'class': 'snow-price_SnowPrice__mainM__azqpin'},
		'link': {'tag': 'a', 'class': 'product-snippet_ProductSnippet__galleryBlock__52z59'},
		'image': {'tag': 'img', 'class': 'gallery_Gallery__image__re6q0q', 'attribute': 'src'},
		'generic_quantity': {'tag': 'span', 'class': 'snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography-Secondary__base__1i67dw snow-ali-kit_Typography__sizeTextM__1shggo SnowSearchHeading_SnowSearchHeading__count__b9qvy'},
		'obj_components': ['titles', 'integers', 'links', 'images'],
		'fields': ['title', 'price', 'link', 'image']
	}
}