FROM python:3.9.20-alpine3.19
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements-prd.txt .

RUN apk add --update --no-cache --virtual dependencies  build-base openssl-dev libffi-dev mariadb-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del dependencies
RUN apk add --no-cache mariadb-connector-c

COPY entrypoint.sh .
COPY src .
VOLUME /usr/src/app/media/
EXPOSE 8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
