FROM python:3.6-alpine

ENV PYTHONUNBUFFERED=0

RUN apk add curl e2fsprogs-extra

COPY src/requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Creating working directory
RUN adduser -S appuser
RUN mkdir /app
COPY src/ /app
COPY flag.txt /app/flag.txt
RUN chmod -R 755 /app/
USER appuser

EXPOSE 8800

WORKDIR /app
CMD waitress-serve --port=8800 main:app
