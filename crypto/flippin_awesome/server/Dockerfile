FROM python:3.6-alpine

ENV PYTHONUNBUFFERED=0

COPY requirements.txt /tmp

RUN apk add --no-cache --virtual .build-deps python3-dev gcc musl-dev libffi-dev libressl-dev
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN apk del .build-deps

# Creating working directory
RUN adduser -S appuser
RUN mkdir /app
COPY src/ /app/
RUN chown -R root:root /app
USER appuser

EXPOSE 5000

WORKDIR /app
ENV FLASK_APP=server.py
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
