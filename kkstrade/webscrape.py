from bs4 import BeautifulSoup
import requests
from operator import itemgetter
from urllib.request import Request, urlopen

def techmall(search):
	try:
		techmall_link = 'https://www.techmall.com.ng'
		response = requests.get('{}/?s={}&page=search&post_type=product'.format(techmall_link, search))
		soup = BeautifulSoup(response.text, 'html.parser')
		items = soup.find_all(class_='inner-wrap nasa-title-bottom')
		try:
			products_list= []
			for item in items:
				products = {}
				if (' '.join(search.split('+')).lower() or ''.join(search.split('+')).lower()) in item.find('a')['title'].lower():
					name = item.find('a')['title']
					link = item.find('a')['href']
					image = item.img['src']
					price = item.find(class_='price').get_text()
					products['name'] = name
					products['link'] = link
					products['image'] = image
					products['price'] = int(price.replace('₦','').replace(',','').split(' ')[0])
					products['store'] = 'Tech Mall'
					products['color'] = '#2170ba'
					total_list.append(products)
				else:
					continue
		except KeyError as e:
			pass
	except Exception as e:
		print(str(e))

def ziksales(search):
	try:
		ziksales_link = 'https://ziksales.com/'

		response = requests.get('{}/search?item={}'.format(ziksales_link,search))
		soup = BeautifulSoup(response.text, 'html.parser')
		items = soup.find_all(class_='card card-product')
		try:
			products_list = []
			for item in items:
				products = {}
				if (' '.join(search.split('+')).lower() or ''.join(search.split('+')).lower()) in item.find_all('a')[1].get_text().lower():
					name = item.find_all('a')[1].get_text()
					link = item.find_all('a')[1]['href']
					image = item.img['src']
					price = item.find(class_='price').get_text()
					products['name'] = name
					products['link'] = link
					products['image'] = image
					products['price'] = int(price.strip('₦').replace(',','').split('₦')[1])
					products['store'] = 'Zik Sales'
					products['color'] = '#f15523'
					total_list.append(products)
				else:
					continue
		except KeyError:
			pass
	except:
		pass

def payporte(search):
	try:
		payporte_link = 'https://payporte.com'

		response = requests.get('{}/catalogsearch/result/?q={}'.format(payporte_link,search))

		soup = BeautifulSoup(response.text, 'html.parser')

		items = soup.find_all(class_='product-item-info')

		try:
			products_list = []
			for item in items:
				products = {}
				if (' '.join(search.split('+')).lower() or ''.join(search.split('+')).lower()) in item.findAll('a')[1].get_text().strip('\n').lower():
					name = item.findAll('a')[1].get_text().strip('\n')
					link = item.findAll('a')[1]['href']
					image = item.img['src']
					if item.find(class_='price') == None:
						price = 'Out of stock'
					else:
						price = item.find(class_='price').get_text()
					products['name'] = name
					products['link'] = link
					products['image'] = image
					products['store'] = 'Payporte'
					products['color'] = '#e8592d'
					if price != 'Out of stock':
						products['price'] = int(price.strip('₦').replace('.00','').replace(',','').split()[0])
					else:
						products['price'] = 0
					total_list.append(products)
				else:
					continue
				
		except KeyError:
			pass
	except:
		pass

def jumia(search):
	try:
		jumia_link = 'https://www.jumia.com.ng'
		jumia_deep_link = [R'https://c.jumia.io/?a=24732&c=11&p=r&E=kkYNyk2M4sk%3D&ckmrdr=https%3A%2F%2F','&utm_campaign=24732']

		response = requests.get('{}/catalog/?q={}'.format(jumia_link,search))
		soup = BeautifulSoup(response.text, 'html.parser')

		items = soup.find_all(class_='core')
		
		products_list = []
		newlist = []
		try:
			for item in items:
				products = {}
				if (' '.join(search.split('+')).lower() or ''.join(search.split('+')).lower()) in item.find(class_='name').get_text().lower():
					name = item.find(class_='name').get_text()
					price = item.find(class_='prc').get_text()
					image = item.find('img')['data-src']
					link = jumia_link+item['href']#jumia_deep_link[0]+jumia_link+item['href']+jumia_deep_link[1]
					products['name'] = name
					products['price'] = int(price.strip('₦ ').replace(',','').split()[0])
					products['image'] = image
					products['link'] = link
					products['store'] = 'Jumia'
					products['color'] = '#ff9900'
					total_list.append(products)
				else:
					continue
		except KeyError:
			pass
	except:
		pass

def get_data(search_input):
	global total_list
	total_list = []
	search = '+'.join(search_input.split())

	payporte(search)
	jumia(search)
	ziksales(search)
	techmall(search)

	total_list = sorted(total_list, key=itemgetter('price'))

	return total_list
