#!/bin/bash

OUTPUT=graph.csv

rm -f OUTPUT

########### nodes ############

# dirs
for i in `find . -type d | grep -v "\\.git" | grep -v "\\.$"`
do echo "d|cic:/$i" | sed "s/\\.\///g" >> $OUTPUT
done

# objects
for i in `find .  -regex ".*\.\(con\|ind\|var\)\.xml\.gz$"`
do echo "o|cic:/$i" | sed "s/\\.\///g" | sed "s/\\.xml\\.gz$//g" >> $OUTPUT
done

########### edges ############

# dirs into dirs
for i in `find . -type d`
do (cd $i;
    for j in `find . -maxdepth 1 -type d`
    do echo "dd|cic:/$i|cic:/$i/$j"
    done) | grep -v "\\.$" | grep -v "\\.git" | sed "s/\\.\///g" >> $OUTPUT
done

# objects into dirs
for i in `find . -type d`
do (cd $i;
    for j in `find . -maxdepth 1 -regex ".*\.\(con\|ind\|var\)\.xml\.gz$"`
    do echo "od|cic:/$i|cic:/$i/$j"
    done) | grep -v "\\.git" | sed "s/\\.\///g" | sed "s/\\.xml\\.gz$//g" >> $OUTPUT
done

# objects into objets
for i in `find . -name "*.xml.gz"`
do (for j in `zcat $i | grep "cic:" | sed "s/.*\"\(cic:[^\"]*\)\".*/\\1/" | sort -u`
    do echo "oo|cic:/$i|$j"
    done) | sed "s/\\.\///g" | sed "s/\\.body\\.xml\\.gz//g" | sed "s/\\.types\\.xml\\.gz//g" | sed "s/\\.xml\\.gz//g" >> $OUTPUT
done

# remove duplicates

sort -u $OUTPUT > $OUTPUT.tmp && mv $OUTPUT.tmp $OUTPUT

# add dependcy arcs between files
cat $OUTPUT | grep oo | sed "s/^oo/ii/g" | sed "s/\/[^|\/]*|/|/g" | sed "s/\/[^\/]*$//g" | sort -u >> $OUTPUT
