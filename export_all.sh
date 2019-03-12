#!/bin/bash

# TODO befor running the script:
#  opam init
#  opam repo add coq-released https://coq.inria.fr/opam/released
# in the coq directory
#  opam pin -n .
#  opam install --deps-only coq

# REMEMBER TO CLEAN THE XML DESTINATION DIRECTORY RECURSIVELY
#  - how to do that safely in the script?

LOCAL_XML_ROOT="$(pwd)/xml"
LOCAL_XML_ROOT_SAVED="$(pwd)/xml.saved"
XML_ROOT="/tmp/xml"
MKGRAPH="$(pwd)/mkgraph.sh"
ALLPACKAGESNO=$(opam list -a --repos coq-released --short | wc -l)
#PACKAGES=$(opam list -a --installable --repos coq-released --short -S | grep -v coqide)
PACKAGES=$(cat TODO)
echo "Installable packages (out of $ALLPACKAGESNO total Coq packages) to be exported: $PACKAGES"
rm -rf "$LOCAL_XML_ROOT_SAVED"
mv "$LOCAL_XML_ROOT" "$LOCAL_XML_ROOT_SAVED"
rm -rf "$XML_ROOT"
mkdir -p "$XML_ROOT" "$LOCAL_XML_ROOT"
for i in $PACKAGES
do
        export COQ_XML_LIBRARY_ROOT="$XML_ROOT/$i"
        mkdir "$COQ_XML_LIBRARY_ROOT"
        echo "Exporting $i to $COQ_XML_LIBRARY_ROOT"
        opam uninstall "$i" --yes > /dev/null
	(yes no | /usr/bin/time opam install "$i" > "$COQ_XML_LIBRARY_ROOT/opam.log" 2>&1) || touch "$COQ_XML_LIBRARY_ROOT/ABORTED"
        #(cd "$COQ_XML_LIBRARY_ROOT" && $MKGRAPH)
	mv "$COQ_XML_LIBRARY_ROOT" "$LOCAL_XML_ROOT"
done
