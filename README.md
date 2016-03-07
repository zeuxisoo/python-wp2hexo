# Python WP2Hexo

A simple converter for my wordpress post to hexo

# Installation

Create environment

	make venv

Export wordpress post and replace the `data/_export.xml`

	cp -Rf wordpress-*.xml data/_export.xml

Run the convert script

	make run

Finally, move the `_posts` to hexo source directory

	cp -Rf data/_posts/* /path/to/hexo/source/_posts/
