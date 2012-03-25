#!/usr/bin/env bash
PROJECT="Products.RefBiblioParser"
IMPORT_URL="git@github.com:collective/repo:Products.RefBiblioParser.git"
cd $(dirname $0)/..
[[ ! -d t ]] && mkdir t
rm -rf t/*
tar xzvf $(ls -1t ~/cgwb/$PROJECT*z) -C t
files="
./
"
for f in $files;do
    rsync -aKzv t/$PROJECT/$f $f
done
# vim:set et sts=4 ts=4 tw=80: 
