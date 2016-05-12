FROM geometalab/gdal-docker

USER root

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y curl nano sqlite3 python3-pip \
    && apt-get autoremove -y && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# allow use of gosu to execute commands as different user
RUN mkdir -p /usr/local/bin && \
    curl -o /usr/local/bin/gosu -sSL https://github.com/tianon/gosu/releases/download/1.8/gosu-amd64 && \
    chmod +x /usr/local/bin/gosu

ENV DATA_DIR=/data OUTPUT_DIR=/output APP_DIR=/app STATICFILES_DIR=/staticfiles

COPY docker/entrypoint.sh /entrypoint.sh
COPY requirements.txt $APP_DIR/requirements.txt
RUN pip3 install -r $APP_DIR/requirements.txt

COPY GeoConverter $APP_DIR/GeoConverter
COPY static $APP_DIR/static
COPY templates $APP_DIR/templates
COPY manage.py $APP_DIR/manage.py
COPY OGRgeoConverter $APP_DIR/OGRgeoConverter
RUN chmod +x /entrypoint.sh
RUN mkdir -p $STATICFILES_DIR
RUN chown -R nobody:nogroup $APP_DIR $STATICFILES_DIR

# map volumes to persist databases, generated output and even map in app source
VOLUME ["$DATA_DIR", "$OUTPUT_DIR", "$APP_DIR"]

WORKDIR $APP_DIR
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["dummy"]
