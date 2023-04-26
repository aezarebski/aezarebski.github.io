#!/usr/bin/env bash

git add index.html

# A bunch of boring lists
git add lists/books.html
git add lists/links.html
git add lists/movies-and-series.html
git add lists/quotes.html
git add lists/zarebski.bib

# The TikZ gallery
git add misc/tikz/gallery.html

for ix in $(seq -f "%02g" 1 2);
do
    git add ./misc/tikz/fig$ix.png
done

# The basegraphicsR gallery
git add misc/basegraphicsR/gallery.html

for ix in $(seq -f "%02g" 1 5);
do
    git add ./misc/basegraphicsR/fig$ix.png
done

# The ggplot2 gallery
git add misc/ggplot2/gallery.html

for ix in $(seq -f "%02g" 1 11);
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
git add notes/academic-journal-notes.html
git add notes/beast2-notes.html
git add notes/colour-notes.html
git add notes/docker-notes.html
git add notes/emacs-lisp-notes.html
git add notes/git-notes.html
git add notes/glossary-biology.html
git add notes/glossary-mathematics-and-statistics.html
git add notes/latex-notes.html
git add notes/org-mode-notes.html
git add notes/phylogenetics-notes.html
git add notes/probability-notes.html
git add notes/python-notes.html
git add notes/r-notes.html
git add notes/tutoring-notes.html

# The nicemacs stuff
git add misc/nicemacs/nicemacs.html
