#!/bin/sh

PREFIX=$1
XMLROOT=$2
LIBRARY=$3

# Clone library repo
git clone --depth 1 "$LIBRARY"

export PATH=$PREFIX/bin:$PATH

# Build and install the library
export COQEXTRAFLAGS=-xml
export COQ_XML_LIBRARY_ROOT=$XMLROOT
make
make install