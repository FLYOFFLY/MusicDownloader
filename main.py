import urllib.request
import urllib.error
import http.client
import html.parser;

import os

LINK_MUSICS = ['http://muzmo.ru/get/music', "'http://muzmo.ru/get/cat_music"]
LINK_ATTRBS = '/artist_songs?artist_id'
ATRB_MUSIC = ("class", 'block')
ATRB_MUSICURL = ("class", 'block')
ATRB_ALBULMURL = ("class", 'block')
ATRB_ARTISTBUTTON = ("class", 'btn_short_border')
LINK_SITE = ['http://muzmo.ru']

class MyParser(html.parser.HTMLParser):
	def __init__(self):
		self.list = {}
		self.artist_id = 0
		super(MyParser, self).__init__()
	def handle_starttag(self, tag, attrs):
		if "a" in tag:
			if len(attrs) > 0 and attrs[0][0] == "class":
				if len(attrs) <= 1:
					return
				path = attrs[1][1];
				if attrs[0] == ATRB_MUSIC:
					for LINK_MUSIC in LINK_MUSICS:
						if	LINK_MUSIC in attrs[1][1]:
							countSymbolSub = len(LINK_MUSIC)
							symbolTilda = attrs[1][1][countSymbolSub::].find("/")
							idMusic = attrs[1][1][countSymbolSub:symbolTilda+countSymbolSub:]
							if idMusic not in self.list:
								self.list[idMusic] = attrs[1][1]
				elif attrs[0] == ATRB_ARTISTBUTTON and LINK_ATTRBS in path:
							self.artist_id = (path[path.index("=")+1:path.index("&"):])

	def update(self):

		for r in range(len(self.list)):
			self.list[r] = self.list[r][5::]


class ParserMusic(html.parser.HTMLParser):
	def __init__(self,artist_id):
		self.list = []
		self.artist_id = artist_id
		super(ParserMusic,self).__init__()
	def handle_starttag(self, tag, attrs):
		if "a" in tag:
			if len(attrs)>0 and attrs[0] == ATRB_MUSICURL and len(attrs)>1 and '/info?' in attrs[1][1]:
				parserart = MyParser()
				parserart.feed(str(urllib.request.urlopen(LINK_SITE+attrs[1][1]).read()))
				for r in parserart.list.values():
					if parserart.artist_id == self.artist_id:
						self.list.append(r)

class ParserAlbium(html.parser.HTMLParser):
	def __init__(self,artist_id):
		self.list = {}
		self.artist_id = artist_id
		super(ParserAlbium,self).__init__()
	def handle_starttag(self, tag, attrs):
		if "a" in tag:
			if len(attrs)>0 and attrs[0] == ATRB_ALBULMURL and len(attrs)>1 and '/album?' in attrs[1][1]:
				parserart = ParserMusic(self.artist_id)
				parserart.feed(str(urllib.request.urlopen(LINK_SITE+attrs[1][1]).read()))
				try:
					for r in parserart.list:
						self.list[r[r.rindex("/")+1:r.rindex("mp3")-1:]]=r
						print(r)
				except:
					pass


artist_id = ["32423"]
for art_id in artist_id:
	parser = ParserAlbium(art_id)
	parser.feed(str(urllib.request.urlopen(
		"http://muzmo.ru/artist_songs?mod=1&artist_id="+art_id).read()))
	print(len(parser.list))
	for fileName in parser.list.keys():
		print(fileName)

		resource =  urllib.request.urlopen(parser.list[fileName])
		try:
			with open(fileName+".mp3", "wb") as musicFile:
				musicFile.write(resource.read())
		except:
			pass