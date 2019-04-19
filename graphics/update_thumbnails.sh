#!/bin/bash

# notes: as of late 2018, this takes about 1.5 minutes to run. 

# usage.
if [ ! -d "${1}" ]; then
  echo "usage: update_thumbnails.sh <directory>"
  echo "e.g. /home/chester/public_html/images/photoalbum. The photoalbum"
  echo "directory should contain subdirectories like aluminum, residential,"
  echo "etc. Those directories should each contain a directory called orig."
  echo "this script will make directories called fullsize and thumbnails in"
  echo "each awning style directory, sized appropriately for the website."
  exit
fi

# loop over the subdirectories in the photoalbum directory.
for d in `ls "${1}"`; do
  echo "${d}"

  # delete the fullsize directory if it exists.
  if [ -d "${1}/${d}/fullsize" ]; then
    rm -rdf "${1}/${d}/fullsize"
  fi
  # make the fullsize directory.
  mkdir "${1}/${d}/fullsize"
 
  # delete the thumbnails directory if it exists.
  if [ -d "${1}/${d}/thumbnails" ]; then
    rm -rdf "${1}/${d}/thumbnails"
  fi
  mkdir "${1}/${d}/thumbnails"
 
  # loop over the files in each "orig" directory.
  find "${1}/${d}/orig" -type f | while read f; do
    # get the basename of the file.
    b=`basename "${f}"`

    # fullsize images should fit into a box of the dimensions below.
    convert "${1}/${d}/orig/${b}" -resize 975x500\> -unsharp 0.25x0.25+8+0.065 "${1}/${d}/fullsize/${b}"

    # thumbnails should be 48x48. 
    convert "${1}/${d}/orig/${b}" -thumbnail 48x48^ -unsharp 0.25x0.25+8+0.065 -gravity center -extent 48x48 "${1}/${d}/thumbnails/${b}"
  done
done
