FROM python:3.7-alpine
ARG WORKDIR
ENV WORKDIR_IN ${WORKDIR}
RUN apk update && \
    apk add python python-dev linux-headers libffi-dev gcc make musl-dev py-pip mysql-client git openssl-dev

WORKDIR $WORKDIR
RUN mkdir -p $WORKDIR /var/log/CTFd /var/uploads

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . $WORKDIR

RUN for d in CTFd/plugins/*; do \
      if [ -f "$d/requirements.txt" ]; then \
        pip install -r $d/requirements.txt; \
      fi; \
    done;

RUN chmod +x $WORKDIR/docker-entrypoint.sh


EXPOSE 8000
ENTRYPOINT ${WORKDIR_IN}/docker-entrypoint.sh
