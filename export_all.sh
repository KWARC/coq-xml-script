#!/bin/bash

# TODO befor running the script:
#  opam repo add coq-released https://coq.inria.fr/opam/released
# in the coq directory
#  opam pin -n .

# BUG? make clean required in the coq directory

# REMEMBER TO CLEAN THE XML DESTINATION DIRECTORY RECURSIVELY
#  - how to do that safely in the script?

XML_ROOT="$(pwd)/xml"
MKGRAPH="$(pwd)/mkgraph.sh"
PACKAGES=$(opam list -a --repos coq-released --short -S | grep -v coqide)
for i in $PACKAGES
do
        export COQ_XML_LIBRARY_ROOT="$XML_ROOT/$i"
        mkdir "$COQ_XML_LIBRARY_ROOT"
        echo "Exporting $i to $COQ_XML_LIBRARY_ROOT"
        opam uninstall "$i" --yes > /dev/null
        opam install "$i" > "$COQ_XML_LIBRARY_ROOT/opam.log" 2>&1 || touch "$COQ_XML_LIBRARY_ROOT/ABORTED"
        (cd "$COQ_XML_LIBRARY_ROOT" && $MKGRAPH)
done
