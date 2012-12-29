# Direcotry structure look like

	wpconvert
	- /_posts
	- /lib
	- /octopress
	- /hexo
	- convert.py
	- run.sh
	- export.xml

# Login wordpress, export the XML files place into root driectory and named

	export.xml

# Make a directory to store converted post

	mkdir _posts && chmod 777 _posts

# Clone octopress in current directory and install it

	git clone git://github.com/imathis/octopress.git octopress
	cd octopress

	> [Y/n] yes
	rvm gemset create octopress
	rvm gemset use octopress
	gem install bundler
	bundle install
	rake install

# Run convert script 

- convert each post into _posts directory
- and remove all old posts from octopress _post directory
- and then copy all converted _posts into octopress _post directory

	cd ..
	bash run.sh

# Bulid and Preview

	cd octopress
	rake generate
	rake preview

# Copyright

	Creative Commons License 3.0 (BY-NC-SA)

	BY: Attribution, NC: NonCommercial, SA: ShareAlike