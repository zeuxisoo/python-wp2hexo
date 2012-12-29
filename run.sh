#!/bin/bash

stop=0

select convertor in octopress hexo quit; do
	if [ $convertor = "octopress" ]; then
		echo -e "\033[;35;5mConverting..."
		python convert-to-octopress.py
	elif [ $convertor = "hexo" ]; then
		echo -e "\033[;35;5mConverting..."
		python convert-to-hexo.py
	elif [ $convertor = "quit" ]; then
		stop=1
	fi
	break
done

if [ $stop = 0 ]; then
	echo -e "\033[;35;5mRemoving..."
	rm -Rf octopress/source/_posts/*
	
	echo -e "\033[;35;5mCopying..."
	cp -Rf _posts/* octopress/source/_posts/
	
	echo -e "\033[;32;5mDone"
fi