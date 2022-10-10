#!/usr/bin/env bash

# A bunch of boring lists
git add lists/books.html
git add lists/links.html
git add lists/movies-and-series.html
git add lists/quotes.html
git add lists/zarebski.bib

# The ggplot2 gallery
git add misc/ggplot2/gallery.html

for ix in $(seq -f "%02g" 1 8);
do
    git add ./misc/ggplot2/fig$ix.png
done

# The d3 gallery
git add misc/d3/gallery.html

for ix in $(seq -f "%02g" 1 5);
do
    git add ./misc/d3/fig$ix.js
done

# A bunch of notes files
git add notes/r-notes.html
git add notes/tutoring-notes.html
