echo -e "\033[;35;5mConverting..."
python convert.py

echo -e "\033[;35;5mRemoving..."
rm -Rf octopress/source/_posts/*

echo -e "\033[;35;5mCopying..."
cp -Rf _posts/* octopress/source/_posts/

echo -e "\033[;32;5mDone"