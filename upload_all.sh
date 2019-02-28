#!/bin/bash

# Read the token as an argument
token=$2

# Read the group
group=$1

# Create a directory to move done stuff two
mkdir done

for name in $(find -maxdepth 1 -name 'coq-*' | cut -c 3-); do
  echo "Uploading $name";
  gitlab-force-upload -dest "$group/$name" -token "$token" -folder "$name" -url "https://gl.mathhub.info" -v;  
  mv $name/ done/;
done
