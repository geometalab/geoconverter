FROM geometalab/gdal-docker

USER root

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y curl sqlite3 python3-pip git \
    && apt-get autoremove -y && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# allow use of gosu to execute commands as different user
RUN mkdir -p /usr/local/bin && \
    curl -o /usr/local/bin/gosu -sSL https://github.com/tianon/gosu/releases/download/1.9/gosu-amd64 && \
    chmod +x /usr/local/bin/gosu

ENV DATA_DIR=/data OUTPUT_DIR=/output APP_DIR=/app \
    STATICFILES_DIR=/staticfiles HONCHO_STARTFILE=Procfile.django

COPY docker/entrypoint.sh /entrypoint.sh
COPY requirements.txt $APP_DIR/requirements.txt
RUN pip3 install -r $APP_DIR/requirements.txt

COPY .git $APP_DIR/.git
RUN cd $APP_DIR && git reset --hard
# replace dynamic version info with fixed values
RUN cd $APP_DIR && git checkout -- setup.py setup.cfg versioneer.py \
    && python3 setup.py build_py -d . \
    && rm -rf .* docker circle.yml MANIFEST.in setup.* versioneer.py || true
RUN chmod +x /entrypoint.sh
RUN mkdir -p $STATICFILES_DIR
RUN chown -R nobody:nogroup $APP_DIR $STATICFILES_DIR

# map volumes to persist databases, generated output and even map in app source
VOLUME ["$DATA_DIR", "$OUTPUT_DIR", "$APP_DIR"]

WORKDIR $APP_DIR
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["honcho", "-f", "$HONCHO_STARTFILE", "start"]
