#!/bin/bash -xe

nbdir=notebooks
builddir=_build

if [ ! -d $builddir ]; then
    mkdir $builddir
fi

for f in $nbdir/*.ipynb; do
    # execute notebook and export to HTML
    jupyter nbconvert "$f" --template=templates/nbextensions --execute --to html --output-dir $builddir
done

for f in $builddir/*.html; do
    # replace links to local ipynb files with links to html files
    sed -i 's/.ipynb/.html/g' "$f"
done
