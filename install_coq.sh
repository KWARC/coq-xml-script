#!/bin/sh

PREFIX=$1
XMLROOT=$2

# Prerequisites, install via
# opam install ocamlfind camlp5 num

# Clone coq repo
git clone --depth 10 --branch csc_plugin https://github.com/sacerdot/coq
cd coq || exit
git checkout 7f1c9e439

# Configure with the given prefix
./configure -prefix=$PREFIX

# Build coq + xml
export COQ_XML=-xml
export COQ_XML_LIBRARY_ROOT=$XMLROOT
yes | make -j4