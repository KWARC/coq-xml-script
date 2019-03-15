#!/bin/bash

TMP=ops.tmp
DEST=$(pwd)/coqdoc-output

# per-library coqdoc rendering
#HERE=`pwd`
#for lib in `ls`; do
	#cd $HERE/$lib
	#rm -r $TMP *.html coqdoc.css
	#for i in `ls .. | grep -v $lib`; do echo "-external ../$i ????????? >> $TMP ; done
	#COMMAND="`cat $TMP` `find . -name "*.v"`"
	#echo $COMMAND | xargs coqdoc
	#rm $TMP
#done

# global coqdoc rendering
cd xml
rm -r $TMP *.html coqdoc.css
for i in `ls`; do echo "-R $i \"\"" >> $TMP ; done
COMMAND="`cat $TMP` `find . -name "*.v"`"
echo $COMMAND | xargs coqdoc
rm $TMP
rm $DEST/*
mv *.html coqdoc.css "$DEST"
