#!/bin/bash

# Read the token as an argument
token=$2

# Read the group
group=$1

# Create a directory to move done stuff two
mkdir done

for name in $(find -maxdepth 1 -name 'coq-*' | cut -c 3-); do
  echo "Uploading $name";
  python script.py $token $name $group;  
  mv $name/ done/;
done
