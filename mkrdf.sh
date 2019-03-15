#!/bin/bash

cd xml
for i in *
do
	echo "$i"
	(cd $i && cat graph.csv | ../../coqscripts/extract all -doc ../../coqdoc-output/index.html -csv | sort -u > triples.csv && cat triples.csv | ../../coqscripts/extract mkxml > triples.rdf)
done
