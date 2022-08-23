import requests
from appPublic.http_client import Http_Client
from appPublic.timeUtils import curDateString
from uninews.baseprovider import BaseProvider
from .version import __version__
app_info = {}

def set_app_info(appkey):
	app_info.update({
		'appkey':appkey
	})

def buildProvider(newsfeed):
	print(f'TheNewsApi version {__version__}')
	return NewsApi(newsfeed)

class NewsApi(BaseProvider):
	def __init__(self, newsfeed):
		self.newsfeed = newsfeed
		self.appkey = app_info.get('appkey')

	def get_result_mapping(self):
		return {
			'total':'totalResults',
			'articles':'articles'
		}
	
	def get_article_mapping(self):
		return {
			'link':'url',
			'img_link':'urlToImage',
			'publish_date':'publishedAt'
		}
	
	def news(self, q=None, 
						categories=[],
						countries=[], 
						language=[], 
						page=0):
		url = 'https://newsapi.org/v2/everything'
		hc = Http_Client()
		keyword = q
		if keyword == '':
			keyword = None
		categories = None if len(categories) == 0 else categories[0]
		language_str = None if len(language) == 0 else language[0]
		countries_str = None if len(countries) == 0 else countries[0]
		today = curDateString()
		p = {
			'apiKey':self.appkey,
			'language':language_str,
			'from':today,
			'to':today,
			'pageSize':100,
			'page':page,
			'q':keyword
		}
		x = hc.get(url, params=p)
		return x
		return self._newscall(url, q, categories=categories,
					countries=countries,
					language=language, 
					page=page)

	def topstory(self, q=None, categories=[],
						countries=[], language=[], page=0):
		url = 'https://newsapi.org/v2/top-headlines'
		hc = Http_Client()
		keyword = q
		if keyword == '':
			keyword = None
		categories = None if len(categories) == 0 else categories[0]
		language_str = None if len(language) == 0 else language[0]
		countries_str = None if len(countries) == 0 else countries[0]
		today = curDateString()
		print(categories, language_str)
		p = {
			'apiKey':self.appkey,
			'category':categories, 
			'country':countries_str,
			'pageSize':100,
			'page':page,
			'q':keyword
		}
		# 'sources':'bbc-news'
		# 'language':language_str,
		# 'from':today,
		# 'to':today,
		print('url=', url, 'params=', p)
		x = hc.get(url, params=p)
		return x

if __name__ == '__main__':
	print('input appkey:')
	appkey=input()
	set_app_info(appkey)
	nc = NewsApi()
	while True:
		print('key word to search news, ":quit" to exit')
		x = input()
		if x == ':quit':
			break
		news = nc.getNews(x)
		print(news.keys())
		print(news['results'][0].keys())
