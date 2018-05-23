from bs4 import BeautifulSoup
import urllib  
import urllib.error
import urllib.request
import urllib.parse 
import os  
import re
import zlib
import datetime



directory = 'G:/PixivCrawling/'


def get_cookies():
	with open("cookies.txt", 'r') as f:
		_cookies = ''
		for row in f.read().split('\n'):
			k, v = row.strip().split(':', 1)
			k = k.strip()
			v = v.strip()
			_cookies = _cookies + k +'='+ v + ';'
		return _cookies


def get_IDlist(date):
	
	url = 'https://www.pixiv.net/ranking.php?mode=daily&date='+date
	headers = {
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.4601.400 QQBrowser/10.0.515.400',
				'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding':'gzip, deflate, br',
				'accept-language':'zh-CN,zh;q=0.9',
				'dnt':'1',
				'Cookie':get_cookies()
			}

	req = urllib.request.Request(url=url, headers=headers)
	data = urllib.request.urlopen(req).read()
	decompressed_data = zlib.decompress(data, 16+zlib.MAX_WBITS).decode('utf8')


	soup = BeautifulSoup(decompressed_data,'html.parser')

	initlist = soup.select('img[data-type="illust"]')

	IDlist = []
	
	for ID in initlist:
		ID = re.findall(r"data-id=\"(\d*)\"",str(ID))
		IDlist.append(ID[0])
	return IDlist
	



def get_image(ID):

	url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+str(ID)
	headers = {
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.4601.400 QQBrowser/10.0.515.400',
				'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding':'gzip, deflate, br',
				'accept-language':'zh-CN,zh;q=0.9',
				'dnt':'1',
				'Cookie':get_cookies()
			}

	req = urllib.request.Request(url=url, headers=headers)
	data = urllib.request.urlopen(req).read()
	decompressed_data = zlib.decompress(data, 16+zlib.MAX_WBITS).decode('utf8')

	soup = BeautifulSoup(decompressed_data,'html.parser')

	taglist = soup.select('img[class="original-image"]')
	
	if len(taglist)==0:
		return None
	
	url = re.findall(r"data-src=\"(.*?)\"",str(taglist[0]))[0]

	headers = {
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.4601.400 QQBrowser/10.0.515.400',
				'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'accept-encoding':'gzip, deflate, br',
				'accept-language':'zh-CN,zh;q=0.9',
				'dnt':'1',
				'referer':'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+str(ID),
				'Cookie':get_cookies()

			}
	req = urllib.request.Request(url=url, headers=headers)
	data = urllib.request.urlopen(req).read()
	filename = url.split('/')[-1]

	save_file(file_directory=directory,file_name=directory+filename,data=data)



def save_file(file_directory,file_name, data):  
	if data == None:  
		return
	if not os.path.exists(file_directory):
		os.makedirs(file_directory)
	file = open(file_name, "wb")
	file.write(data)
	file.flush()
	file.close()

	#Judgement 
	if os.path.getsize(file_name) < 2:
		os.remove(file_name)

		target = Image.new('RGBA', (UNIT_SIZE, UNIT_SIZE), (255,255,255,0))
		
		quality_value = 100

		target.save(file_name, quality = quality_value)
	
	print (file_name + '  '+ str(os.path.getsize(file_name))+'bytes')   

	return None








if __name__=="__main__":



	begin = datetime.date(2018,1,1)  
	end = datetime.date(2018,5,1)  
	date = begin
	delta = datetime.timedelta(days=1)


	while date <= end:
		for ID in get_IDlist(date.strftime("%Y%m%d")):
			get_image(ID)
		date += delta




	#The standard url of daily ranking list
	#url = 'https://www.pixiv.net/ranking.php?mode=daily&date='+'20150303'

	#The standard url of single picture
	#url = 'https://i.pximg.net/img-original/img/2015/05/27/00/01/31/50577795_p0.png'
	
	#url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=50577795'
	#save_file(r'C:\Users\Administrator\Desktop','1.png',get_image(url))





	
	








