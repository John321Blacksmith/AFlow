agents = [
	'Mozilla/5.0 (Linux; Android 5.0.1; LG-D332 Build/LRX22G) AppleWebKit/534.47 (KHTML, like Gecko)  Chrome/48.0.2206.146 Mobile Safari/537.1',
	'Mozilla/5.0 (Windows; Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/50.9',
	'Mozilla/5.0 (U; Linux i683 x86_64; en-US) Gecko/20100101 Firefox/71.2',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 8_9_7) AppleWebKit/601.38 (KHTML, like Gecko) Chrome/53.0.2245.340 Safari/535',
	'Mozilla/5.0 (Linux; Android 7.1.1; LG-H910 Build/NRD90M) AppleWebKit/602.37 (KHTML, like Gecko)  Chrome/48.0.2118.264 Mobile Safari/600.7',
	'Mozilla/5.0 (Linux; Linux x86_64) AppleWebKit/601.30 (KHTML, like Gecko) Chrome/55.0.2865.344 Safari/533',
	'Mozilla/5.0 (Android; Android 7.1.1; Xperia V Build/NDE63X) AppleWebKit/602.22 (KHTML, like Gecko)  Chrome/48.0.3704.195 Mobile Safari/600.8',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 9_9_6; like Mac OS X) AppleWebKit/534.50 (KHTML, like Gecko)  Chrome/51.0.2831.131 Mobile Safari/537.3',
	'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G935I Build/LMY47X) AppleWebKit/603.20 (KHTML, like Gecko)  Chrome/49.0.3991.330 Mobile Safari/535.8',
	'Mozilla/5.0 (Android; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/602.4 (KHTML, like Gecko)  Chrome/55.0.3724.336 Mobile Safari/534.6'
]


# the confs DS with xpath elements
scraping_data = {
    'source': 'https://books.toscrape.com/',
    'links_file': 'books.csv',
    'object': '//article[@class="product_pod"]',
    'title': '//a/@title',
    'image': '//img[@class="thumbnail"]/@src',
    'link': '//a/@href',
    'price': '//p[@class="price_color"]',
    'fields': ['title', 'image', 'link', 'price'],
    'n_p_element': '.next > a:nth-child(1)',
    'n_p_slug': 'catalogue/page-',
}

auction_site = {
	'source': 'https://nedradv.ru/nedradv/ru/auction',
	'table': '.g-color-black-opacity-0_6',
	'row': 'tr',
	'link': 'a',
	'object': '/html/body/main/section[3]/div/div[1]/div[1]',
	'date': './/div[1]/h1',
	'square': './/div[1]/p',
	'region': './/div[1]/h1',
	'status': './/dl[1]/dd',
	'submit_deadline': './/dl[8]',
	'contribution': './/dl[4]',
	'organizer': './/dl[6]',
	'n_p_element': '.u-pagination-v1-4--active',
	'months': ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'],
}