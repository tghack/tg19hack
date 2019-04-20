FROM python:3.6-alpine

ENV PYTHONUNBUFFERED=0

COPY src/requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Creating working directory
RUN adduser -S appuser
RUN mkdir /app
COPY src/ /app
RUN chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "-u", "/app/manage.py", "runserver", "0.0.0.0:8000"]
