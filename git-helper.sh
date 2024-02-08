#!/usr/bin/env bash

git add git-helper.sh
git add notes.html
git add index.html
git add microgram.css

# A bunch of boring lists
git add lists/books.html
git add lists/links.html
git add lists/movies-and-series.html
git add lists/quotes.html
git add lists/zarebski.bib

# The plotnine gallery
git add misc/plotnine/gallery.html

for ix in $(seq -f "%02g" 1 5);
do
    git add ./misc/plotnine/fig$ix.png
done

# The TikZ gallery
git add misc/tikz/gallery.html

for ix in $(seq -f "%02g" 1 8);
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
git add notes/linux-notes.html
git add notes/org-mode-notes.html
git add notes/phylogenetics-notes.html
git add notes/probability-notes.html
git add notes/pypfilt-notes.html
git add notes/python-notes.html
git add notes/r-notes.html
git add notes/tutoring-notes.html
git add notes/workflow-notes.html

# The nicemacs stuff
git add misc/nicemacs/nicemacs.html
git add misc/nicemacs/nicemacs-v2.html

# The recipes
git add misc/recipes/img/*.png
git add misc/recipes/index.html
git add misc/recipes/recipe-style.css
git add misc/recipes/butternut-squash-risotto.html
git add misc/recipes/paneer-korma.html

# Teaching things
git add teaching/index.html
git add teaching/teaching.css

# ML blog posts
git add misc/ml/index.html
git add misc/ml/post-2024-01-03.html
git add misc/ml/post-2024-01-04.html
git add misc/ml/post-2024-01-07.html
git add misc/ml/post-2024-01-09.html
git add misc/ml/post-2024-01-11.html
git add misc/ml/post-2024-01-25.html
git add misc/ml/example-2024-01-25/coverage.png
git add misc/ml/example-2024-01-25/loss.png
git add misc/ml/post-2024-02-08.html
git add misc/ml/example-2024-02-08/loss.png

# DERP page
git add derp/index.html
git add derp/styles.css
