#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from datetime import datetime

try:
	import feedparser
except ImportError:
	from lib import feedparser

feedparser.SANITIZE_HTML = 0
#feedparser._HTMLSanitizer.acceptable_elements.append('coolcode')

class Parser(object):
	def parse(self):
		feed = feedparser.parse("export.xml")

		for entry in feed.entries:
			if entry.wp_status == "publish" and entry.wp_post_type == "post":
				wordpress_id = entry.wp_post_id
				date = datetime.strptime(entry.wp_post_date, "%Y-%m-%d %H:%M:%S")
				name = "%02d-%02d-%02d-%s.markdown" % (date.year, date.month, date.day, wordpress_id)

				date_string = "%02d-%02d-%02d" % (date.year, date.month, date.day)
				title_string = entry.title.replace("'", '&#39;')

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

				print("Converting: %s" % name)

				f = open("_posts/%s" % name, 'w+')
				f.write("---\n")
				f.write("layout: post\n")
				f.write("title: '%s'\n" % title_string.encode("utf8"))
				f.write("date: %s\n" % date_string)
				f.write("wordpress_id: %s\n" % wordpress_id)
				f.write("permalink: /blog/archives/%s\n" % wordpress_id)
				f.write("comments: true\n")
				f.write("---\n")
				f.write(content.encode("utf8"))
				f.close()

if __name__ == "__main__":
	Parser().parse()