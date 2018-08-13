FROM python:2.7-alpine
LABEL maintainer="Goran Nushkov" \
      maintainer_email="gnuskov@protonmail.com"

RUN apk update && apk add build-base postgresql-dev

ENV INSTALL_PATH /flexio
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "flexio.app:create_app()"
