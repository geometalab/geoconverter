#!/bin/sh

OLDDIR=${1:-geoconverter-www}
NEWDIR=${2:-$(ls -td1 geoconverter-20* | head -1)}

(cd "$OLDDIR" && find -name '*.sqlite' | tar cf - -T - static/admin ) | ( cd "$NEWDIR" && tar tvf - )

