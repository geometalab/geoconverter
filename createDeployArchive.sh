#!/bin/sh

git archive --prefix=geoconverter`date +-%Y-%m-%d`/ HEAD | gzip > geoconverter.`date +%Y%m%d`.tar.gz

