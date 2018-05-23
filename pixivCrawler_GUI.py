import pixivCrawler
import datetime
import _thread
import os

from kivy.uix.boxlayout import BoxLayout  

from kivy.core.window import Window  
from kivy.app  import App  
from kivy.clock import Clock

from kivy.uix.textinput import TextInput


class pixivCrawlerApp(App):  



	def build(self):
		self.newImage = ''
		self.dateToday = datetime.date.today() - datetime.timedelta(days=2)
		self.root.ids.from_year.text = str(self.dateToday.year)
		self.root.ids.from_month.text = str(self.dateToday.month)
		self.root.ids.from_day.text  = str(self.dateToday.day)
		self.root.ids.to_year.text = str(self.dateToday.year)
		self.root.ids.to_month.text = str(self.dateToday.month)
		self.root.ids.to_day.text = str(self.dateToday.day)
		self.isCrawling = False
		
	def print(self,text):
		self.root.ids.console.text = self.root.ids.console.text + text + os.linesep


	def startCrawling(self):
		if(self.isCrawling):
			return
		else:	
			_thread.start_new_thread(self.crawl,())
		

	def crawl(self):
		try:
			begin = datetime.date(int(self.root.ids.from_year.text),int(self.root.ids.from_month.text),int(self.root.ids.from_day.text)) 
			end = datetime.date(int(self.root.ids.to_year.text),int(self.root.ids.to_month.text),int(self.root.ids.to_day.text))  
			date = begin
			delta = datetime.timedelta(days=1)
			directory = self.root.ids.dir.text

			if(begin > end):
				self.print('Please check your input!')
				return
			if(end > self.dateToday):
				date = self.dateToday
		except:
			self.print('Please check your input!')
			return


		self.print('Mission Start!')
		self.isCrawling = True	
		self.root.ids.startButton.text = 'Crawling.......'	

		try:
			while (date <= end and self.isCrawling):

				self.print('----'+str(date)+'----')

				IDlist = pixivCrawler.get_IDlist(date.strftime("%Y%m%d"))

				self.print(str(len(IDlist))+' Pictures:')

				for ID in IDlist:
					newImage = pixivCrawler.get_image(ID,directory)
					if(newImage!=None):
						self.newImage = newImage
						self.print(newImage)
						Clock.schedule_once(self.refreshImage)

				date += delta
			
			self.print('Mission Accomplished!')
		except:
			self.print('Mission Interrupted!')
			self.print('Please check your \'cookies.txt\'.')
		finally:
			self.isCrawling = False



	def refreshImage(self,dt):
		self.root.ids.newImage.source = self.newImage





if __name__ == '__main__':  
	pixivCrawlerApp().run() 










	
	








