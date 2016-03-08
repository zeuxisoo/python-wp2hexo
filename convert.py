#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import feedparser
from datetime import datetime

class Convert(object):

    def __init__(self):
        self.export_file = "data/export.xml"
        self.post_file   = "data/_posts/{0}.md"

        self.english_tags = {
            '伺服器'   : 'Server',
            '忽然一感' : 'Life',
            '未分類'   : 'Other',
            '案子'     : 'Case',
            '程式作品' : 'Project',
            '程式修改' : 'Code Modifiy',
            '程式片段' : 'Code Snippet',
            '程式筆記' : 'Notes',
            '網摘'     : 'Bookmark',
            '網絡見聞' : 'Web Link',
            '網路代碼' : 'Web Coding',
            '網路文章' : 'Web Article',
            '編輯器'   : 'Editor',
            '資料收集' : 'Research',
            '軟體應用' : 'Software'
        }

    def parse(self):
        export_feed = feedparser.parse(self.export_file)

        export_feed.entries.reverse()

        for entry in export_feed.entries:
            if entry.wp_status == "publish" and entry.wp_post_type == "post":
                title            = self.format_title(entry.title)
                date             = self.format_date(entry.wp_post_date)
                wordpress_id     = entry.wp_post_id
                tags, categories = self.format_categories_and_tags(entry.tags)
                content          = self.format_content(entry.content[0].value)

                #
                filename = "{0}-{1}".format(date, wordpress_id)

                #
                post_file = open(self.post_file.format(filename), 'w+')
                post_file.write("---\n")
                post_file.write("layout      : post\n")
                post_file.write("title       : \"{0}\"\n".format(title))
                post_file.write("date        : {0}\n".format(date))
                post_file.write("wordpress_id: {0}\n".format(wordpress_id))
                # post_file.write("permalink   : /blog/archives/{0}\n".format(wordpress_id))
                post_file.write("comments    : true\n")
                post_file.write("categories  : \n\n")
                post_file.write("{0}\n\n".format(categories))
                post_file.write("tags        : \n\n")
                post_file.write("{0}\n\n".format(tags))
                post_file.write("---\n\n")
                post_file.write(content)
                post_file.close()

    def format_title(self, title):
        return title.replace("\\", "\\\\")

    def format_date(self, post_date):
        format_datetime = datetime.strptime(post_date, "%Y-%m-%d %H:%M:%S")
        convert_to_date = "%02d-%02d-%02d" % (format_datetime.year, format_datetime.month, format_datetime.day)

        return convert_to_date

    def format_categories_and_tags(self, tags):
        temp_categories = []
        temp_tags       = []

        for tag in tags:
            if tag.scheme == "category":
                key = tag.term
                if key in self.english_tags:
                    temp_categories.append("- " +  self.english_tags[key])
                else:
                    temp_tags.append("- " +  key)

        return ["\n".join(sorted(temp_tags)), "\n".join(sorted(temp_categories))]

    def format_content(self, content):
        content = re.sub(r'^<pre[^>]*>$', '{% codeblock %}' + "\n", content)
        content = re.sub(r'^<\/pre>$', "\n" + '{% endcodeblock %}' + "\n", content)

        content = re.sub(r'<code[^>]*>', '{% codeblock %}', content)
        content = re.sub(r'<\/code>', '{% endcodeblock %}', content)

        content = re.sub(r'<coolcode.*[download="(.*)"]?.*lang="(.*)">', r'{% codeblock lang:\1 %}', content)
        content = re.sub(r'<coolcode lang=(.*)>', r'{% codeblock lang:\1 %}', content)
        content = re.sub(r'<coolcode>', r'{% codeblock %}', content)
        content = re.sub(r'<\/coolcode>', r'{% endcodeblock %}', content)

        content = re.sub(r'{% codeblock lang:(.*)" linenum="(on|off)" download="link2code.html %}', r'{% codeblock lang:\1 %}', content)
        content = re.sub(r'{% codeblock lang:(.*)" linenum="(on|off) %}', r'{% codeblock lang:\1 %}', content)
        content = re.sub(r'{% codeblock lang:(.*)" download="(.*) %}', r'{% codeblock lang:\1 %}', content)

        content = re.sub(r'{% codeblock lang:(txt|text|dtd|bash) %}', "{% codeblock %}", content)

        content = re.sub(r'<!-- raw -->', r"{% raw %}", content)
        content = re.sub(r'<!-- endraw -->', r"{% endraw %}", content)

        content = re.sub(r'<raw>', r"{% raw %}", content)
        content = re.sub(r'</endraw>', r"{% endraw %}", content)

        content = content.replace(u"# 參考", u"##### 參考:")
        content = content.replace('< %', '<%')
        content = content.replace('< ?php', '<?php')

        return content

if __name__ == "__main__":
    convert = Convert()
    convert.parse()
