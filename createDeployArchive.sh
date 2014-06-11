#!/bin/sh

git archive --prefix=geoconverter`date +-%Y-%m-%d-%H%M%S`/ HEAD | gzip > geoconverter.`date +%Y%m%d%H%M%S`.tar.gz

