FROM python:3.6-alpine
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

CMD gunicorn -c "python:config.gunicorn" "flexio.app:create_app()"
