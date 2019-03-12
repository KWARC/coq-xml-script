#!/bin/bash

# Read the token as an argument
token=$2

# Read the group
group=$1

# Create directories to move finished things to
mkdir success
mkdir failed

for name in $(find -maxdepth 1 -name 'coq-*' | cut -c 3-); do
  echo "Uploading $name";
  if gitlab-force-upload -pro -dest "$group/$name" -token "$token" -folder "$name" -url "https://gl.mathhub.info" -v; then  
    mv $name/ success/;
  else
    mv $name/ failed/;
  fi;
done
