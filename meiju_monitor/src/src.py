#encoding: utf-8


#if __name__ == "__main__":
#	 main()

class Monitor(object):
# Monitor functions as a crawler
	def __init__(self, series_name, home_page="http://www.ttmeiju.com"):
		self.series_name = series_name #name of target series
		self.home_page = home_page
		episodes = self.read_url(url)

	def read_url(self, addr):
		import urllib2
		import re
		try:
			page = urllib2.urlopen(addr)
		except urllib2.HTTPError:
			raise ValueError, 'invalid address'

		content = page.read()
		pattern = r'<tr class="scontent">[\s\S]*</tr>'
		#this means each section starts with <tr class="scontent">, and ends with
		#</tr>
		#TODO 150119: this pattern returns all <tr class="scontent">...</tr> as one
		#match, needs to be fixed
		result = []
		try:
			for i in re.finditer(pattern,content.lower()):
				result.append(i.group())
		except AttributeError:
			raise ValueError,'RE pattern error'
		return result

	#def url_generate(self):
	#	#generate a url base on template and series name
	#	name = self.series_name
	#	temp = self.url_template
	#	url=temp.replace('TO_BE_NAMED',name).lower()
#    	#return url

	def episode_parser(self,lstEpisodes):
		#this function parses all name and SxEx from episodes
		import re
		pattern = r'\<a href="(?P<seed_url>.*seed.*\.html)"\>\n(?P<episode_name>.*)\</a\>' 
		#this means <a href="ADDR">\nSERIES_NAME</a>
		#150119 notice: there is a \n right after <a href=xxxx>
		result = []
		for i in lstEpisodes:
			tmp = re.search(pattern,i)
			epi_name, epi_addr = tmp.group('episode_name'), tmp.group('seed_url')
			result.append((epi_name,epi_addr))
			#yield (epi_name,epi_addr)
			#TODO 150119: study how to do yield instead of return

		return result
	#url=self.__url_generate()
	#episodes=self.__read_url(url)