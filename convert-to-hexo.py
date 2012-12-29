#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)

sys.setdefaultencoding("utf-8")

import unicodedata
import re
import urllib2
from datetime import datetime

try:
	import feedparser
except ImportError:
	from lib import feedparser

feedparser.SANITIZE_HTML = 0
#feedparser._HTMLSanitizer.acceptable_elements.append('coolcode')

class Parser(object):
	URL = 'http://translate.google.com.hk/translate_a/t?client=t&hl=zh-TW&sl=zh-CN&tl=en&ie=UTF-8&oe=UTF-8&multires=1&otf=2&ssel=3&tsel=3&sc=1'
	HEADER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'

	def translate(self, input):
		search_url = self.URL + '&text=' + urllib2.quote(input.encode("UTF8"))
		req = urllib2.Request(search_url)
		req.add_header('User-Agent', self.HEADER_AGENT)
		r = urllib2.urlopen(req)
		value = r.read().split('"')[1]
		return value
		
	def seo_string(self, x):
		r = unicodedata.normalize('NFKD',x).encode('cp1256','ignore')
		r = unicode(re.sub('[^\w\s-]','',r).strip().lower())
		r = re.sub('[-\s]+','-',r)
		return r

	def parse(self):
		feed = feedparser.parse("export.xml")

		feed.entries.reverse()

		for entry in feed.entries:
			if entry.wp_status == "publish" and entry.wp_post_type == "post":
				wordpress_id = entry.wp_post_id
				date = datetime.strptime(entry.wp_post_date, "%Y-%m-%d %H:%M:%S")
				date_string = "%02d-%02d-%02d" % (date.year, date.month, date.day)
				title_string = entry.title.replace("'", '&#39;')
				
				title = re.sub(r'-(.*)-', r'\1', self.seo_string(self.translate(title_string).replace(" ", "-").decode("UTF8")))
				name = "%s.md" % (title)
				
				#name = "%02d-%02d-%02d-%s.markdown" % (date.year, date.month, date.day, wordpress_id)

				content = entry.content[0].value
				content = re.sub(r'^<pre[^>]*>$', '{% codeblock %}' + "\n", content)
				content = re.sub(r'^<\/pre>$', "\n" + '{% endcodeblock %}' + "\n", content)
				content = re.sub(r'<code[^>]*>', '{% codeblock %}', content)
				content = re.sub(r'<\/code>', '{% endcodeblock %}', content)
				
				content = re.sub(r'<coolcode.*[download="(.*)"]?.*lang="(.*)">', r'{% codeblock lang:\1 %}', content)
				content = re.sub(r'<\/coolcode>', r'{% endcodeblock %}', content)

				content = re.sub(r'{% codeblock lang:(.*)" linenum="on %}', r'{% codeblock lang:\1 %}', content)
				content = re.sub(r'{% codeblock lang:(txt|text|dtd|bash) %}', "{% codeblock %}", content)

				content = content.replace(u"# 參考", u"##### 參考:")
				content = content.replace('< %', '<%')
				content = content.replace('< ?php', '<?php')

				to_english_tags = {
					u'伺服器'	: 'Server',
					u'忽然一感'	: 'Life',
					u'未分類'	: 'Other',
					u'案子'		: 'Case',
					u'程式作品'	: 'Project',
					u'程式修改'	: 'Code Modifiy',
					u'程式片段'	: 'Code Snippet',
					u'程式筆記'	: 'Notes',
					u'網摘'		: 'Bookmark',
					u'網絡見聞'	: 'Web Link',
					u'網路代碼'	: 'Web Coding',
					u'網路文章'	: 'Web Article',
					u'編輯器'	: 'Editor',
					u'資料收集'	: 'Research',
					u'軟體應用'	: 'Software'
				}

				tags = []
				for tag in entry.tags:
					if tag.scheme == "category":
						key = tag.term
						if key in to_english_tags:
							tags.append("- " +  to_english_tags[key])
						else:
							tags.append("- " +  key.encode('utf8'))

				print("Converting: %s" % (name))

				f = open("_posts/%s" % name, 'w+')
				f.write("---\n")
				f.write("layout: post\n")
				f.write("title: '%s'\n" % title_string.encode("utf8"))
				f.write("date: %s\n" % date_string)
				f.write("wordpress_id: %s\n" % wordpress_id)
				#f.write("permalink: /blog/archives/%s\n" % wordpress_id)
				f.write("comments: true\n")
				f.write("categories:\n")
				f.write("%s\n" % "\n".join(tags))
				f.write("---\n")
				f.write(content.encode("utf8"))
				f.close()

if __name__ == "__main__":
	Parser().parse()