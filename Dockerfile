#--- Release ---
FROM python:3.7-alpine
COPY --from=d0g3/h1ve /root/.cache /root/.cache
COPY --from=d0g3/h1ve requirements.txt .
COPY --from=d0g3/h1ve /usr/bin/mysqladmin /usr/bin/mysqladmin
RUN pip install -r requirements.txt && rm -rf /root/.cache

ARG WORKDIR
ENV WORKDIR_IN ${WORKDIR}
WORKDIR $WORKDIR
RUN mkdir -p $WORKDIR /var/log/CTFd /var/uploads
COPY . $WORKDIR

RUN for d in CTFd/plugins/*; do \
      if [ -f "$d/requirements.txt" ]; then \
        pip install -r $d/requirements.txt; \
      fi; \
    done;

RUN chmod +x $WORKDIR/docker-entrypoint.sh


EXPOSE 8000
ENTRYPOINT ${WORKDIR_IN}/docker-entrypoint.sh
