#!/usr/bin/env bash
PROJECT="Products.RefBiblioParser"
IMPORT_URL="git@github.com:collective/repo:Products.RefBiblioParser.git"
cd $(dirname $0)/..
[[ ! -d t ]] && mkdir t
rm -rf t/*
tar xzvf $(ls -1t ~/cgwb/$PROJECT*z) -C t
files="
*cfg
setup.py
src/*/*/tests/
src/*/*/con*zcml
src/*/*/testing.py
src/*/*/profiles/
"
for f in $files;do
    rsync -aKzv t/$PROJECT/$f $f
done

cat >> base.cfg << EOF

[buildout]
auto-checkout += Products.CMFBibliographyAT
sources-dir = \${buildout:directory}/src.mrdeveloper
[sources]
Products.CMFBibliographyAT = svn http://svn.plone.org/svn/collective/bibliograph.core/trunk

EOF
# vim:set et sts=4 ts=4 tw=80: 
