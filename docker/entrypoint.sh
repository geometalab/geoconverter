#!/bin/bash
set -e

if [ "$1" = 'dummy' ]; then
  chown -R nobody:nogroup $DATA_DIR $OUTPUT_DIR $STATICFILES_DIR

  if ! test -f $DATA_DIR/default.sqlite; then
    gosu nobody python3 manage.py syncdb --noinput
    test -z "$DJANGO_ADMIN_USER" && (echo "DJANGO_ADMIN_USER env variable not set, aborting!"; exit 1)
    echo "from django.contrib.auth.models import User;" \
         "User.objects.create_superuser(\"$DJANGO_ADMIN_USER\", \"$DJANGO_ADMIN_EMAIL\", \"$DJANGO_ADMIN_PASS\")" | \
         gosu nobody python3 manage.py shell
  fi
  if ! test -f $DATA_DIR/sessions.sqlite; then
    gosu nobody python3 manage.py syncdb --database=sessions_db
  fi
  if ! test -f $DATA_DIR/ogrgeoconverter.sqlite; then
    gosu nobody python3 manage.py syncdb --database=ogrgeoconverter_db
    gosu nobody python3 manage.py loaddata ogr_formats.json --database=ogrgeoconverter_db
    gosu nobody python3 manage.py loaddata global_shell_parameters.json --database=ogrgeoconverter_db
  fi
  if ! test -f $DATA_DIR/log.sqlite; then
    gosu nobody python3 manage.py syncdb --database=ogrgeoconverter_log_db
  fi
  if ! test -f $DATA_DIR/conversionjobs.sqlite; then
    gosu nobody python3 manage.py syncdb --database=ogrgeoconverter_conversion_jobs_db
  fi

#python3 manage.py migrate && \
  gosu nobody sh -c 'python3 manage.py collectstatic --noinput && \
    python3 manage.py runserver 0.0.0.0:8000'
fi
exec "$@"
